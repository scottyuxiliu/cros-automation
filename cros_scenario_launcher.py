import os, sys, select, logging, argparse, time, errno, pathlib, subprocess
import paramiko

from cros_constants import TEST_SYS_AUTOTEST_PATH, SCENARIOS

class CrosScenarioLauncher():
    """[summary]
    """

    def __init__(self, ip, username, ssh_private_key_file, debug):
        self.logger = logging.getLogger("cros_automation.CrosScenarioLauncher")
        fh = logging.FileHandler("cros_scenario_launcher.log") # to overwrite existing log file, use mode="w"
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s') # output method name too
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        self.logger.debug("--------------------------------------------------------------------------------")
        self.logger.debug(f"establishing ssh connection with the test system")
        self.logger.debug("--------------------------------------------------------------------------------")

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.logger.debug(f"fetch ssh private key file {ssh_private_key_file}")
        ssh_private_key = paramiko.RSAKey.from_private_key_file(ssh_private_key_file)

        self.logger.debug(f"connect to test system with the following details")
        self.logger.debug(f"hostname = {ip}")
        self.logger.debug(f"username = {username}")
        self.logger.debug(f"ssh_private_key_file = {ssh_private_key_file}")

        # try:
        #     self.ssh.connect(hostname=ip, username=username, pkey=ssh_private_key)
        #     self.logger.debug("ssh session established!")
        # except paramiko.AuthenticationException:
        #     self.logger.error(f"paramiko authentication failed when connecting to {ip}. it may be possible to retry with different credentials.")
        #     sys.exit(1)
        # except paramiko.SSHException:
        #     self.logger.error(f"paramiko ssh exception when connecting to {ip}. there might be failures in SSH2 protocol negotiation or logic errors.")
        #     sys.exit(1)

        self.ssh.connect(hostname=ip, username=username, pkey=ssh_private_key)
        self.logger.debug("ssh session established!")

        self.ip = ip
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
        """this will be blocking.

        Args:
            stdout ([type]): [description]

        Returns:
            list: [description]
        """

        content = []

        if stdout.channel.recv_exit_status() != 0:
            self.logger.error(f"{'(DEBUG MODE) ' if self.debug else ''}stdout.channel.recv_exit_status() returned {stdout.channel.recv_exit_status()}")

        for line in stdout.readlines():
            line = line.rstrip("\n")
            self.logger.debug(f"{'(DEBUG MODE) ' if self.debug else ''}{line}")
            content.append(line)

        return content

    
    # The double underscore __ prefixed to a variable makes it private. It gives a strong suggestion not to touch it from outside the class.
    # Python performs name mangling of private variables. Every member with a double underscore will be changed to _object._class__variable. So, it can still be accessed from outside the class, but the practice should be refrained.
    def __exec_command(self, command, read_stdout=False):
        """execute command using paramiko ssh.exec_command().

        if self.debug is true or read_stdout is true, this will be blocking and stdout will be read.

        Args:
            command (str): command to be executed
            read_stdout (bool, optional): if true, paramiko ssh.exec_command() will be blocking and stdout will be read. Defaults to False.
        """
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command) # non-blocking call
        except paramiko.SSHException:
            self.logger.error("(DEBUG MODE) paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")
        else:
            if self.debug is True or read_stdout is True:
                self.__read_stdout(stdout) # if debug flag is true or read_stdout is true, capture stdout from exec_command. this is blocking.
            else:
                n = len(command.split(";")) # get the number of commands that should be executed
                time.sleep(n) # exec_command does not work properly without this. every additional command requires one more second of wait time.
                self.logger.info("started on the test system")


    # The double underscore __ prefixed to a variable makes it private. It gives a strong suggestion not to touch it from outside the class.
    # Python performs name mangling of private variables. Every member with a double underscore will be changed to _object._class__variable. So, it can still be accessed from outside the class, but the practice should be refrained.
    def __exec_command_local(self, command, read_stdout=False, password=None):
        """execute command locally using subprocess.

        if self.debug is true or read_stdout is true, this will be blocking and stdout will be read.

        Args:
            command (str): command to be executed
            read_stdout (bool, optional): if true, paramiko ssh.exec_command() will be blocking and stdout will be read. Defaults to False.
        """
        if read_stdout is True:
            content = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8")
            self.logger.info(content)
        else:
            subprocess.Popen(command, shell=True)


    # The double underscore __ prefixed to a variable makes it private. It gives a strong suggestion not to touch it from outside the class.
    # Python performs name mangling of private variables. Every member with a double underscore will be changed to _object._class__variable. So, it can still be accessed from outside the class, but the practice should be refrained.
    def __exec_command_in_cros_sdk_chroot(self, command, password):
        """this will be blocking.

        Args:
            command (str): [description]
            password (str): [description]
        """
        channel = self.ssh.invoke_shell()
        channel.send("cd ~/chromiumos/\n")
        time.sleep(1)


        channel.close()
        # channel.send("cros_sdk\n")
        # time.sleep(1)
        # channel.send(f"{password}\n")
        # time.sleep(1)



    def __exist_local(self, path):
        p = self.__read_path(path)
        # self.logger.info(p)

        if p.is_file():
            # self.logger.info("True")
            return True
        else:
            # self.logger.info("False")
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
        self.logger.info(f"{'(DEBUG MODE) ' if self.debug else ''}test connection to {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")

        status = self.ssh.get_transport().is_active()
        if status is True:
            self.logger.info(f"{'(DEBUG MODE) ' if self.debug else ''}ssh session is active")

            self.logger.info(f"{'(DEBUG MODE) ' if self.debug else ''}execute echo \"ssh session is active\"")
            self.__exec_command(f"echo \"ssh session is active\"")

        else:
            self.logger.info("ssh session is closed")

        return status


    def launch_scenario(self, scenario):
        """launch the given scenario on the test system
        """

        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"{'(DEBUG MODE) ' if self.debug else ''}launch {scenario} on {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")

        if scenario in SCENARIOS:
            if SCENARIOS[scenario]["method"] == "manual":
                self.logger.info(f"{'(DEBUG MODE) ' if self.debug else ''}execute: {SCENARIOS[scenario]['command']}")
                self.__exec_command(f"{SCENARIOS[scenario]['command']}")
            elif SCENARIOS[scenario]["method"] == "autotest":
                self.logger.info(f"{'(DEBUG MODE) ' if self.debug else ''}execute: cd {TEST_SYS_AUTOTEST_PATH}; bin/autotest {SCENARIOS[scenario]['control']}")
                self.__exec_command(f"cd {TEST_SYS_AUTOTEST_PATH}; bin/autotest {SCENARIOS[scenario]['control']}")
            elif SCENARIOS[scenario]["method"] == "tast":
                if SCENARIOS[scenario]["local"] is True:
                    self.logger.info(f"{'(DEBUG MODE) ' if self.debug else ''}execute locally: cd ~/chromiumos; cros_sdk tast run {self.ip} {scenario}")
                    self.__exec_command_local(f"cd ~/chromiumos; cros_sdk tast run {self.ip} {scenario}")
                else:
                    self.logger.info(f"{'(DEBUG MODE) ' if self.debug else ''}execute remotely (in chroot): tast run {self.ip} {SCENARIOS[scenario]}")

            else:
                pass
        else:
            self.logger.error(f"{scenario} not supported! supported scenarios are:")
            for key in SCENARIOS.keys():
                self.logger.error(key)


    def prepare_scenario(self, scenario):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"{'(DEBUG MODE) ' if self.debug else ''}prepare {scenario} on {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")

        if scenario in SCENARIOS:
            if SCENARIOS[scenario]["method"] == "autotest":
                # if the control file exists locally, replace the one on the DUT or just upload to the DUT.
                if self.__exist_local(f"./autotest/{SCENARIOS[scenario]['control']}"):
                    if self.__exist_remote(f"{TEST_SYS_AUTOTEST_PATH}/{SCENARIOS[scenario]['control']}"):
                        self.logger.info(f"{'(DEBUG MODE) ' if self.debug else ''}replace {TEST_SYS_AUTOTEST_PATH}/{SCENARIOS[scenario]['control']} with ./autotest/{SCENARIOS[scenario]['control']}")
                    else:
                        self.logger.info(f"{'(DEBUG MODE) ' if self.debug else ''}upload ./autotest/{SCENARIOS[scenario]['control']} to {TEST_SYS_AUTOTEST_PATH}/{SCENARIOS[scenario]['control']}")
                    self.__upload(f"./autotest/{SCENARIOS[scenario]['control']}", f"{TEST_SYS_AUTOTEST_PATH}/{SCENARIOS[scenario]['control']}")

                # if the control file only exists on the target system, use it as is
                elif self.__exist_remote(f"{TEST_SYS_AUTOTEST_PATH}/{SCENARIOS[scenario]['control']}"):
                    self.logger.info(f"{'(DEBUG MODE) ' if self.debug else ''}use as is: {TEST_SYS_AUTOTEST_PATH}/{SCENARIOS[scenario]['control']}")

                # give error if the control file is missing both locally and on the target system
                else:
                    self.logger.error(f"{'(DEBUG MODE) ' if self.debug else ''}file does not exist! ./autotest/{SCENARIOS[scenario]['control']}")
        else:
            self.logger.error(f"{'(DEBUG MODE) ' if self.debug else ''}{scenario} not supported! supported scenarios are:")
            for key in SCENARIOS.keys():
                self.logger.error(key)
