import os, sys, select, logging, argparse
import paramiko

class CrosScenarios():
    """[summary]
    """

    def __init__(self):
        self.logger = logging.getLogger("cros_automation")
        pass

    def init_ssh_connection(self, test_system_ip_address, test_system_username, ssh_private_key_file=None):
        # self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"establishing ssh connection with the test system ...")
        # self.logger.info("--------------------------------------------------------------------------------")

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            if ssh_private_key_file is not None and ssh_private_key_file.strip(): # If you want to make sure that foo really is a boolean and of value True, use the is operator.
                self.logger.info(f"fetch ssh private key file {ssh_private_key_file}")
                ssh_private_key = paramiko.RSAKey.from_private_key_file(ssh_private_key_file)

                self.logger.info(f"connect to test system with the following details")
                self.logger.info(f"hostname = {test_system_ip_address}")
                self.logger.info(f"username = {test_system_username}")
                self.logger.info(f"ssh_private_key_file = {ssh_private_key_file}")
                ssh.connect(hostname=test_system_ip_address, username=test_system_username, pkey=ssh_private_key)
            else:
                self.logger.info(f"connect to test system with the following details")
                self.logger.info(f"hostname = {test_system_ip_address}")
                self.logger.info(f"username = {test_system_username}")
                ssh.connect(hostname=test_system_ip_address, username=test_system_username)

        except paramiko.AuthenticationException:
            self.logger.info(f"paramiko authentication failed when connecting to {test_system_ip_address}. it may be possible to retry with different credentials.")
        except paramiko.SSHException:
            self.logger.info(f"paramiko ssh exception when connecting to {test_system_ip_address}. there might be failures in SSH2 protocol negotiation or logic errors.")

        return ssh


    def enter_s0i3(self, test_system_ip_address, test_system_username, ssh_private_key_file=None):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"enter s0i3 on the test system ...")
        self.logger.info("--------------------------------------------------------------------------------")

        ssh = self.init_ssh_connection(test_system_ip_address, test_system_username, ssh_private_key_file)

        pass


