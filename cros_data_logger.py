import os, sys, select, logging, argparse, time
import paramiko

class CrosDataLogger():
    """[summary]
    """

    def __init__(self, test_system_ip_address, test_system_username, ssh_private_key_file=None):
        self.logger = logging.getLogger("cros_automation.CrosDataLogger")

        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"establishing ssh connection with the test system ...")
        self.logger.info("--------------------------------------------------------------------------------")

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.stdin = None
        self.stdout = None
        self.stderr = None

        try:
            if ssh_private_key_file is not None and ssh_private_key_file.strip(): # If you want to make sure that foo really is a boolean and of value True, use the is operator.
                self.logger.info(f"fetch ssh private key file {ssh_private_key_file}")
                ssh_private_key = paramiko.RSAKey.from_private_key_file(ssh_private_key_file)

                self.logger.info(f"connect to test system with the following details")
                self.logger.info(f"hostname = {test_system_ip_address}")
                self.logger.info(f"username = {test_system_username}")
                self.logger.info(f"ssh_private_key_file = {ssh_private_key_file}")
                self.ssh.connect(hostname=test_system_ip_address, username=test_system_username, pkey=ssh_private_key)

                self.logger.info("ssh session established!")
            else:
                self.logger.info(f"connect to test system with the following details")
                self.logger.info(f"hostname = {test_system_ip_address}")
                self.logger.info(f"username = {test_system_username}")
                self.ssh.connect(hostname=test_system_ip_address, username=test_system_username)

                self.logger.info("ssh session established!")

        except paramiko.AuthenticationException:
            self.logger.info(f"paramiko authentication failed when connecting to {test_system_ip_address}. it may be possible to retry with different credentials.")
        except paramiko.SSHException:
            self.logger.info(f"paramiko ssh exception when connecting to {test_system_ip_address}. there might be failures in SSH2 protocol negotiation or logic errors.")


    def __enter__(self):
        return self


    def __exit__(self, exit_type, exit_value, traceback):
        self.ssh.close()


    def test_connection(self):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info("test connection to the test system ...")
        self.logger.info("--------------------------------------------------------------------------------")

        status = self.ssh.get_transport().is_active()
        if status is True:
            self.logger.info("ssh session is active")

            self.logger.info('executing echo "ssh session is active"')
            try:
                self.ssh.exec_command('echo "ssh session is active"') # non-blocking call
            except paramiko.SSHException:
                self.logger.info(f"paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")

            # wait for the command to finish
            while not self.stdout.channel.exit_status_ready():
                time.sleep(1)

            self.logger.debug(f"ssh console output:")
            for line in self.stdout.readlines():
                self.logger.debug(line)

            # if self.stdout.channel.recv_exit_status() == 0: # blocking call
            #     self.logger.debug(f"ssh console output:")
            #     for line in self.stdout.readlines():
            #         self.logger.debug(line)
            # else:
            #     self.logger.error(f"stdout.channel.recv_exit_status() returned {self.stdout.channel.recv_exit_status()}")
        else:
            self.logger.info("ssh session is closed")
        return status


    def launch_atitool_logging(self, duration=60, output_file_name="pm.csv"):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"launching {duration}-second atitool logging on the test system ...")
        self.logger.info("--------------------------------------------------------------------------------")

        self.logger.info(f'executing: cd /usr/local/atitool; ./atitool -i=1 -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput="{output_file_name}"')
        try:
            stdin, stdout, stderr = self.ssh.exec_command(f'cd /usr/local/atitool; ./atitool -i=1 -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput="{output_file_name}"') # non-blocking call

            # wait for the command to finish
            while not stdout.channel.exit_status_ready():
                time.sleep(1)

            # self.logger.debug("stdin:")
            # for line in stdin.readlines():
            #     self.logger.debug(line)
            self.logger.debug("stdout:")
            for line in stdout.readlines():
                self.logger.debug(line)
            self.logger.debug("stderr:")
            for line in stderr.readlines():
                self.logger.debug(line)

        except paramiko.SSHException:
            self.logger.info(f"paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")

        self.logger.info("atitool logging is running on the test system")