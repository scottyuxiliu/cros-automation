import os, sys, select, logging, argparse, time, errno, pathlib
import paramiko

from cros_constants import TEST_SYS_AUTOTEST_PATH, AUTOTEST_SCENARIOS, MANUAL_SCENARIOS

class CrosScenarioLauncher():
    """[summary]
    """

    def __init__(self, test_system_ip_address, test_system_username, ssh_private_key_file, debug):
        self.logger = logging.getLogger("cros_automation.CrosScenarioLauncher")
        fh = logging.FileHandler("cros_scenario_launcher.log") # to overwrite existing log file, use mode="w"
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
    def __caseless_equal(self, left, right):
        return left.lower() == right.lower()


    # The double underscore __ prefixed to a variable makes it private. It gives a strong suggestion not to touch it from outside the class.
    # Python performs name mangling of private variables. Every member with a double underscore will be changed to _object._class__variable. So, it can still be accessed from outside the class, but the practice should be refrained.
    def __read_path(self, path, is_linux=False):
        """read path in string format and convert it to pathlib.Path() object. if is_linux is true, convert it to Linux style path regardless of current Operating System.

        There might be times when you need a representation of a path without access to the underlying file system (in which case it could also make sense to represent a Windows path on a non-Windows system or vice versa). This can be done with PurePath objects.

        Parameters
        ----------
        path : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """
        path.replace("\\", "/")

        if is_linux:
            return pathlib.PurePosixPath(path)
        else:
            return pathlib.Path(path)


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

    
    # The double underscore __ prefixed to a variable makes it private. It gives a strong suggestion not to touch it from outside the class.
    # Python performs name mangling of private variables. Every member with a double underscore will be changed to _object._class__variable. So, it can still be accessed from outside the class, but the practice should be refrained.
    def __exec_command(self, command):
        if self.debug is True:
            try:
                stdin, stdout, stderr = self.ssh.exec_command(command) # non-blocking call
                self.__read_stdout(stdout) # if debug flag is set, capture stdout from exec_command
            except paramiko.SSHException:
                self.logger.error("paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")
            else:
                self.logger.info("finished on the test system")
        else:
            n = len(command.split(";")) # get the number of commands that should be executed

            try:
                self.ssh.exec_command(command) # non-blocking call, thus need to add delay after
            except paramiko.SSHException:
                self.logger.error("paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")
            else:
                time.sleep(n) # exec_command does not work properly without this. every additional command requires one more second of wait time.
                self.logger.info("started on the test system")


    def __exist_local(self, path):
        p = self.__read_path(path)

        if p.is_file():
            return True
        else:
            return False


    def __exist_remote(self, path):
        sftp = self.ssh.open_sftp()

        try:
            sftp.stat(path)
        except IOError as e:
            if e.errno == errno.ENOENT:
                sftp.close()
                return False
        else:
            sftp.close()
            return True


    def __upload(self, local_file_path, remote_file_path):
        """upload file from local_file_path to remote_file_path

        Parameters
        ----------
        local_file_path : str
            [description]
        remote_file_path : str
            [description]
        """
        sftp = self.ssh.open_sftp()
        sftp.put(local_file_path, remote_file_path)
        sftp.close()


    def test_connection(self):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"test connection to the test system {self.test_system_ip_address} ...")
        self.logger.info("--------------------------------------------------------------------------------")

        status = self.ssh.get_transport().is_active()
        if status is True:
            self.logger.info("ssh session is active")

            self.logger.info('execute echo "ssh session is active"')
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


    def launch_scenario(self, scenario):
        """launch the given scenario on the test system
        """

        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"launch {scenario} on the test system {self.test_system_ip_address} ...")
        self.logger.info("--------------------------------------------------------------------------------")

        if scenario in MANUAL_SCENARIOS:
            self.logger.info(f"execute: {MANUAL_SCENARIOS[scenario]['command']}")
            self.__exec_command(f"{MANUAL_SCENARIOS[scenario]['command']}")
        elif scenario in AUTOTEST_SCENARIOS:
            self.logger.info(f"execute: cd {TEST_SYS_AUTOTEST_PATH}; bin/autotest {AUTOTEST_SCENARIOS[scenario]['control']}")
            self.__exec_command(f"cd {TEST_SYS_AUTOTEST_PATH}; bin/autotest {AUTOTEST_SCENARIOS[scenario]['control']}")
        else:
            self.logger.error(f"{scenario} not supported! supported scenarios are {MANUAL_SCENARIOS.keys()}, {AUTOTEST_SCENARIOS.keys()}")


    def prepare_scenario(self, scenario):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"prepare {scenario} on the test system {self.test_system_ip_address} ...")
        self.logger.info("--------------------------------------------------------------------------------")

        if scenario in MANUAL_SCENARIOS:
            pass
        elif scenario in AUTOTEST_SCENARIOS:
            if self.__exist_remote(f"{TEST_SYS_AUTOTEST_PATH}/{AUTOTEST_SCENARIOS[scenario]['control']}"):
                self.logger.info(f"file already exists: {TEST_SYS_AUTOTEST_PATH}/{AUTOTEST_SCENARIOS[scenario]['control']}")
            else:
                if self.__exist_local(f"./autotest/{AUTOTEST_SCENARIOS[scenario]['control']}"):
                    self.logger.info(f"upload ./autotest/{AUTOTEST_SCENARIOS[scenario]['control']} to {TEST_SYS_AUTOTEST_PATH}/{AUTOTEST_SCENARIOS[scenario]['control']}")
                    self.__upload(f"./autotest/{AUTOTEST_SCENARIOS[scenario]['control']}", f"{TEST_SYS_AUTOTEST_PATH}/{AUTOTEST_SCENARIOS[scenario]['control']}")
                else:
                    self.logger.error(f"file does not exist! ./autotest/{AUTOTEST_SCENARIOS[scenario]['control']}")
        else:
            self.logger.error(f"{scenario} not supported! supported scenarios are {MANUAL_SCENARIOS.keys()}, {AUTOTEST_SCENARIOS.keys()}")
