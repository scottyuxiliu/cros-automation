import os, sys, select, logging, argparse, time
import paramiko

class CrosScenarios():
    """[summary]
    """

    def __init__(self, test_system_ip_address, test_system_username, ssh_private_key_file, debug):
        self.logger = logging.getLogger("cros_automation.CrosScenarios")
        fh = logging.FileHandler("cros_scenarios.log", mode="w") # overwrite existing log file
        # fh = logging.FileHandler("cros_scenarios.log")
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s') # output method name too
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        self.logger.debug("--------------------------------------------------------------------------------")
        self.logger.debug(f"establishing ssh connection with the test system ...")
        self.logger.debug("--------------------------------------------------------------------------------")

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.logger.debug(f"fetch ssh private key file {ssh_private_key_file}")
        ssh_private_key = paramiko.RSAKey.from_private_key_file(ssh_private_key_file)

        self.logger.debug(f"connect to test system with the following details")
        self.logger.debug(f"hostname = {test_system_ip_address}")
        self.logger.debug(f"username = {test_system_username}")
        self.logger.debug(f"ssh_private_key_file = {ssh_private_key_file}")

        # try:
        #     self.ssh.connect(hostname=test_system_ip_address, username=test_system_username, pkey=ssh_private_key)
        #     self.logger.debug("ssh session established!")
        # except paramiko.AuthenticationException:
        #     self.logger.error(f"paramiko authentication failed when connecting to {test_system_ip_address}. it may be possible to retry with different credentials.")
        #     sys.exit(1)
        # except paramiko.SSHException:
        #     self.logger.error(f"paramiko ssh exception when connecting to {test_system_ip_address}. there might be failures in SSH2 protocol negotiation or logic errors.")
        #     sys.exit(1)

        self.ssh.connect(hostname=test_system_ip_address, username=test_system_username, pkey=ssh_private_key)
        self.logger.debug("ssh session established!")

        self.test_system_ip_address = test_system_ip_address
        self.debug = debug


    def __enter__(self):
        return self


    def __exit__(self, exit_type, exit_value, traceback):
        self.ssh.close()


    # The double underscore __ prefixed to a variable makes it private. It gives a strong suggestion not to touch it from outside the class.
    # Python performs name mangling of private variables. Every member with a double underscore will be changed to _object._class__variable. So, it can still be accessed from outside the class, but the practice should be refrained.
    def __read_stdout(self, stdout):
        """[summary]

        Parameters
        ----------
        stdout : [type]
            [description]
        """
        if stdout.channel.recv_exit_status() == 0: # blocking call
            self.logger.debug(f"stdout:")
            for line in stdout.readlines():
                self.logger.debug(line)
        else:
            self.logger.error(f"stdout.channel.recv_exit_status() returned {stdout.channel.recv_exit_status()}")


    def test_connection(self):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"test connection to the test system {self.test_system_ip_address} ...")
        self.logger.info("--------------------------------------------------------------------------------")

        status = self.ssh.get_transport().is_active()
        if status is True:
            self.logger.info("ssh session is active")

            self.logger.info('executing echo "ssh session is active"')
            try:
                if self.debug is True:
                    stdin, stdout, stderr = self.ssh.exec_command('echo "ssh session is active"') # non-blocking call
                    self.__read_stdout(stdout)
                else:
                    self.ssh.exec_command('echo "ssh session is active"') # non-blocking call
                    
            except paramiko.SSHException:
                self.logger.info(f"paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")
        else:
            self.logger.info("ssh session is closed")
        return status


    def reboot(self):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"reboot the test system {self.test_system_ip_address} ...")
        self.logger.info("--------------------------------------------------------------------------------")

        self.logger.info("executing: /sbin/reboot -f > /dev/null 2>&1 &")

        if self.debug is True:
            try:
                stdin, stdout, stderr = self.ssh.exec_command("/sbin/reboot -f > /dev/null 2>&1 &")
                self.__read_stdout(stdout)
            except paramiko.SSHException:
                self.logger.error(f"paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")
            else:
                self.logger.info("rebooted test system")
        else:
            try:
                self.ssh.exec_command("/sbin/reboot -f > /dev/null 2>&1 &")
            except paramiko.SSHException:
                self.logger.error(f"paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")
            else:
                self.logger.info("started reboot on the test system")


    def enter_s0i3(self):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"enter s0i3 on the test system {self.test_system_ip_address} ...")
        self.logger.info("--------------------------------------------------------------------------------")

        self.logger.info("executing: echo mem > /sys/power/state")

        if self.debug is True:
            try:
                stdin, stdout, stderr = self.ssh.exec_command("echo mem > /sys/power/state")
                self.__read_stdout(stdout)
            except paramiko.SSHException:
                self.logger.error(f"paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")
            else:
                self.logger.info("test system entered s0i3")
        else:
            try:
                self.ssh.exec_command("echo mem > /sys/power/state")
            except paramiko.SSHException:
                self.logger.error(f"paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")
            else:
                self.logger.info("started s0i3 entry on the test system")


    def launch_power_loadtest(self):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"launch power_loadtest on the test system {self.test_system_ip_address} ...")
        self.logger.info("--------------------------------------------------------------------------------")

        self.logger.info("executing: cd /usr/local/autotest; bin/autotest tests/power_LoadTest/control")

        try:
            if self.debug is True: # if debug flag is set, capture stdout from exec_command
                stdin, stdout, stderr = self.ssh.exec_command("cd /usr/local/autotest; bin/autotest tests/power_LoadTest/control") # non-blocking call
                self.__read_stdout(stdout)
                self.logger.info("finished power_loadtest on the test system")
            else:
                self.ssh.exec_command("cd /usr/local/autotest; bin/autotest tests/power_LoadTest/control") # non-blocking call
                time.sleep(1) # exec_command does not work properly without this. every additional command requires one more second of wait time.
                self.logger.info("started power_loadtest on the test system")

        except paramiko.SSHException:
            self.logger.error(f"paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")


    
    def launch_aquarium(self):
        """launch graphics_WebGLAquarium on the test system

        20s: preparation
        45s: 50 fishes
        45s: 1000 fishes
        """

        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"launch aquarium on the test system {self.test_system_ip_address} ...")
        self.logger.info("--------------------------------------------------------------------------------")

        self.logger.info("executing: cd /usr/local/autotest; bin/autotest tests/graphics_WebGLAquarium/control")
        try:
            if self.debug is True: # if debug flag is set, capture stdout from exec_command
                stdin, stdout, stderr = self.ssh.exec_command("cd /usr/local/autotest; bin/autotest tests/graphics_WebGLAquarium/control") # non-blocking call
                self.__read_stdout(stdout)
                self.logger.info("aquarium finished on the test system")
            else:
                self.ssh.exec_command("cd /usr/local/autotest; bin/autotest tests/graphics_WebGLAquarium/control") # non-blocking call
                time.sleep(1) # exec_command does not work properly without this. every additional command requires one more second of wait time.
                self.logger.info("aquarium started on the test system")
        except paramiko.SSHException:
            self.logger.error(f"paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")

