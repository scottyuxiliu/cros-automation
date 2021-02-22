import os, sys, select, logging, argparse
import paramiko

class CrosScenarios():
    """[summary]
    """

    def __init__(self, test_system_ip_address, test_system_username, ssh_private_key_file=None):
        self.logger = logging.getLogger("cros_automation")

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
        self.logger.info(f"test connection to the test system ...")
        self.logger.info("--------------------------------------------------------------------------------")

        status = self.ssh.get_transport().is_active()
        if status is True:
            self.logger.info("ssh session is active")
        else:
            self.logger.info("ssh session is closed")
        return status


    def enter_s0i3(self):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"enter s0i3 on the test system ...")
        self.logger.info("--------------------------------------------------------------------------------")

        self.logger.info("executing echo mem > /sys/power/state")
        try:
            self.stdin, self.stdout, self.stderr = self.ssh.exec_command("echo mem > /sys/power/state")
        except paramiko.SSHException:
            self.logger.info(f"paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")

        self.logger.debug(f"ssh console output:")
        for line in self.stdout.readlines():
            self.logger.debug(line)

        self.logger.info("test system entered s0i3")


    def launch_power_loadtest(self):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"launching power_loadtest on the test system ...")
        self.logger.info("--------------------------------------------------------------------------------")

        self.logger.info("executing cd /usr/local/autotest")
        try:
            self.stdin, self.stdout, self.stderr = self.ssh.exec_command("cd /usr/local/autotest")
        except paramiko.SSHException:
            self.logger.info(f"paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")

        self.logger.debug(f"ssh console output:")
        for line in self.stdout.readlines():
            self.logger.debug(line)

        self.logger.info("executing bin/autotest tests/power_LoadTest/control")
        try:
            self.stdin, self.stdout, self.stderr = self.ssh.exec_command("bin/autotest tests/power_LoadTest/control")
        except paramiko.SSHException:
            self.logger.info(f"paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")

        self.logger.debug(f"ssh console output:")
        for line in self.stdout.readlines():
            self.logger.debug(line)

        self.logger.info("power_loadtest is running on the test system")

    
    # def launch_aquarium(self):
    #     self.logger.info("--------------------------------------------------------------------------------")
    #     self.logger.info(f"launching aquarium on the test system ...")
    #     self.logger.info("--------------------------------------------------------------------------------")
