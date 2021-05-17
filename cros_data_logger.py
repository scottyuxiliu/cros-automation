import os, sys, select, logging, time, errno, pathlib, stat
import paramiko

from cros_constants import AGT_DIR_PATH, AGT_INTERNAL_DIR_PATH

class CrosDataLogger():
    """[summary]
    """

    def __init__(self, ip, test_system_username, ssh_private_key_file, debug):
        self.logger = logging.getLogger("cros_automation.CrosDataLogger")
        fh = logging.FileHandler("cros_data_logger.log") # to overwrite existing log file, use mode="w"
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s') # output method name too
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        self.logger.debug("--------------------------------------------------------------------------------")
        self.logger.debug(f"establish ssh connection with the test system")
        self.logger.debug("--------------------------------------------------------------------------------")

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.logger.debug(f"fetch ssh private key file {ssh_private_key_file}")
        ssh_private_key = paramiko.RSAKey.from_private_key_file(ssh_private_key_file)

        self.logger.debug(f"connect to test system with the following details")
        self.logger.debug(f"hostname = {ip}")
        self.logger.debug(f"username = {test_system_username}")
        self.logger.debug(f"ssh_private_key_file = {ssh_private_key_file}")

        # try:
        #     self.ssh.connect(hostname=ip, username=test_system_username, pkey=ssh_private_key)
        # except paramiko.AuthenticationException:
        #     self.logger.error(f"paramiko authentication failed when connecting to {ip}. it may be possible to retry with different credentials.")
        # except paramiko.SSHException:
        #     self.logger.error(f"paramiko ssh exception when connecting to {ip}. there might be failures in SSH2 protocol negotiation or logic errors.")

        self.ssh.connect(hostname=ip, username=test_system_username, pkey=ssh_private_key)
        self.logger.debug("ssh session established!")

        self.ip = ip
        self.debug = debug


    def __enter__(self):
        return self


    def __exit__(self, exit_type, exit_value, traceback):
        self.ssh.close()


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

    
    def __read_path(self, path):
        """read path in string format and convert it to pathlib.Path() object with Linux convention

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
        return pathlib.PurePosixPath(path)

        
    def __exist_remote(self, path):
        """if path exists on the remote system, return true. otherwise, return false.

        Parameters
        ----------
        path : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """
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


    def __exec_command(self, command, read_stdout=False, password=None):
        """execute command using paramiko ssh.exec_command().

        if self.debug is true or read_stdout is true, this will be blocking and stdout will be read.

        if password is not none, password will be written through stdin.

        Args:
            command (str): [description]
            read_stdout (bool, optional): if true, paramiko ssh.exec_command() will be blocking and stdout will be read. Defaults to False.
            password (str, optional): password to be written through stdin. Defaults to None.

        Returns:
            list: stdout from paramiko ssh.exec_command()

        """

        try:
            stdin, stdout, stderr = self.ssh.exec_command(command) # non-blocking call

            if password is not None:
                stdin.write(f"{password}\n")
                stdin.flush()
            
        except paramiko.SSHException:
            self.logger.error("paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")

        else:
            if self.debug is True or read_stdout is True:
                stdout = self.__read_stdout(stdout) # if debug flag is true or read_stdout is true, capture stdout from exec_command. this is blocking.
            else:
                n = len(command.split(";")) # get the number of commands that should be executed
                time.sleep(n) # exec_command does not work properly without this. every additional command requires one more second of wait time.
                self.logger.info("started on the test system")

        return stdout # need to return after the try/except/else blocks. python will not go inside the else block if a value is returned in the try block.


    def test_connection(self):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"{'(DEBUG MODE) ' if self.debug else ''}test connection to {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")

        status = self.ssh.get_transport().is_active()
        if status is True:
            self.logger.info("ssh session is active")

            self.logger.info('execute: echo "ssh session is active"')
            try:
                if self.debug is True:
                    stdin, stdout, stderr = self.ssh.exec_command('echo "ssh session is active"') # non-blocking call
                    self.__read_stdout(stdout)
                else:
                    self.ssh.exec_command('echo "ssh session is active"') # non-blocking call
                    
            except paramiko.SSHException:
                self.logger.error("paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")
        else:
            self.logger.info("ssh session is closed")
        return status


    def atitool_prog(self, arguments):
        """atitool path should be /usr/local/atitool

        Parameters
        ----------
        arguments : str
            arguments passed in for atitool to program
        """
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"atitool program with argument(s) {arguments}")
        self.logger.info("--------------------------------------------------------------------------------")

        self.logger.info(f"execute: cd /usr/local/atitool; ./atitool {arguments}")

        if self.debug is True:
            try:
                stdin, stdout, stderr = self.ssh.exec_command(f"cd /usr/local/atitool; ./atitool {arguments}") # non-blocking call
                self.__read_stdout(stdout)
            except paramiko.SSHException:
                self.logger.error("paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")
            else:
                self.logger.info("finished atitool programming on the test system")
        else:
            try:
                self.ssh.exec_command(f"cd /usr/local/atitool; ./atitool {arguments}") # non-blocking call
                time.sleep(1) # exec_command does not work properly without this. every additional command requires one more second of wait time.
            except paramiko.SSHException:
                self.logger.error("paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")
            else:
                self.logger.info("started atitool programming on the test system")


    def atitool_log(self, duration, index, arguments, output_file_name):
        """atitool path should be /usr/local/atitool

        Parameters
        ----------
        duration : int, optional
            [description], by default 60
        output_file_name : str, optional
            [description], by default "pm.csv"
        """
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"atitool log for {duration} seconds on {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")

        if index == 0:
            if arguments is None:
                self.logger.info(f'execute: cd /usr/local/atitool; ./atitool -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput="{output_file_name}"')
                self.__exec_command(f'cd /usr/local/atitool; ./atitool -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput="{output_file_name}"')
            else:
                self.logger.info(f'execute: cd /usr/local/atitool; ./atitool -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput="{output_file_name}" {arguments}')
                self.__exec_command(f'cd /usr/local/atitool; ./atitool -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput="{output_file_name}" {arguments}')
        else:
            if arguments is None:
                self.logger.info(f'execute: cd /usr/local/atitool; ./atitool -i={index} -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput="{output_file_name}"')
                self.__exec_command(f'cd /usr/local/atitool; ./atitool -i={index} -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput="{output_file_name}"')
            else:
                self.logger.info(f'execute: cd /usr/local/atitool; ./atitool -i={index} -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput="{output_file_name}" {arguments}')
                self.__exec_command(f'cd /usr/local/atitool; ./atitool -i={index} -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput="{output_file_name}" {arguments}')


    def agt_log(self, duration, index, arguments, output_file_name):
        """agt path should be {AGT_DIR_PATH}/agt

        Parameters
        ----------
        duration : int
            [description]
        output_file_name : str
            [description]
        """
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"agt log for {duration} seconds on {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")

        if self.__exist_remote(f"{AGT_DIR_PATH}/agt"):
            if index == 0:
                if arguments is None:
                    self.logger.info(f"{'(DEBUG MODE) ' if self.debug else ''}execute: cd /usr/local/agt; ./agt -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput=\"{output_file_name}\"")
                    self.__exec_command(f"cd /usr/local/agt; ./agt -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput=\"{output_file_name}\"")
                else:
                    self.logger.info(f"{'(DEBUG MODE) ' if self.debug else ''}execute: cd /usr/local/agt; ./agt -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput=\"{output_file_name}\" {arguments}")
                    self.__exec_command(f"cd /usr/local/agt; ./agt -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput=\"{output_file_name}\" {arguments}")
            else:
                if arguments is None:
                    self.logger.info(f"{'(DEBUG MODE) ' if self.debug else ''}execute: cd /usr/local/agt; ./agt -i={index} -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput=\"{output_file_name}\"")
                    self.__exec_command(f"cd /usr/local/agt; ./agt -i={index} -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput=\"{output_file_name}\"")
                else:
                    self.logger.info(f"{'(DEBUG MODE) ' if self.debug else ''}execute: cd /usr/local/agt; ./agt -i={index} -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput=\"{output_file_name}\" {arguments}")
                    self.__exec_command(f"cd /usr/local/agt; ./agt -i={index} -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput=\"{output_file_name}\" {arguments}")
        else:
            self.logger.error(f"no such file: {AGT_DIR_PATH}/agt")
    
    
    def agt_internal_log(self, duration, index, arguments, output_file_name):
        """agt_internal path should be {AGT_INTERNAL_DIR_PATH}/agt_internal

        Parameters
        ----------
        duration : int
            [description]
        output_file_name : str
            [description]
        """
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"{'(DEBUG MODE) ' if self.debug else ''}agt internal log for {duration} seconds on {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")

        if self.__exist_remote(F"{AGT_INTERNAL_DIR_PATH}/agt_internal"):
            if index == 0:
                if arguments is None:
                    self.logger.info(f"{'(DEBUG MODE) ' if self.debug else ''}execute: cd /usr/local/agt_internal; ./agt_internal -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput=\"{output_file_name}\"")
                    self.__exec_command(f"cd /usr/local/agt_internal; ./agt_internal -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput=\"{output_file_name}\"")
                else:
                    self.logger.info(f"{'(DEBUG MODE) ' if self.debug else ''}execute: cd /usr/local/agt_internal; ./agt_internal -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput=\"{output_file_name}\" {arguments}")
                    self.__exec_command(f"cd /usr/local/agt_internal; ./agt_internal -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput=\"{output_file_name}\" {arguments}")
            else:
                if arguments is None:
                    self.logger.info(f"{'(DEBUG MODE) ' if self.debug else ''}execute: cd /usr/local/agt_internal; ./agt_internal -i={index} -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput=\"{output_file_name}\"")
                    self.__exec_command(f"cd /usr/local/agt_internal; ./agt_internal -i={index} -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput=\"{output_file_name}\"")
                else:
                    self.logger.info(f"{'(DEBUG MODE) ' if self.debug else ''}execute: cd /usr/local/agt_internal; ./agt_internal -i={index} -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput=\"{output_file_name}\" {arguments}")
                    self.__exec_command(f"cd /usr/local/agt_internal; ./agt_internal -i={index} -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput=\"{output_file_name}\" {arguments}")

        else:
            self.logger.error(f"no such file: {AGT_INTERNAL_DIR_PATH}/agt_internal")
            

    def pac_log(self, duration, password):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"{'(DEBUG MODE) ' if self.debug else ''}pac log for {duration} seconds on {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"{'(DEBUG MODE) ' if self.debug else ''}execute: sudo -S sh -c \"cd ~/pac-db; python3 pac_db2.py -c guybrush_r0_pacs_mainsmt.py -t {duration}\"")
        self.__exec_command(f"sudo -S sh -c \"cd ~/pac-db; python3 pac_db2.py -c guybrush_r0_pacs_mainsmt.py -t {duration}\"", False, password)


    def is_file(self, path):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"check if {path} is a file or a directory")
        self.logger.info("--------------------------------------------------------------------------------")

        path = str( self.__read_path(path) )

        if self.__exist_remote(path):
            sftp = self.ssh.open_sftp()
            if stat.S_ISDIR( sftp.stat(path).st_mode ):
                self.logger.info(f"{path} is a directory")
                return False
            else:
                self.logger.info(f"{path} is a file")
                return True
        else:
            self.logger.error(f"no such file or directory: {path}")


    def move_file(self, remote_file_path, remote_dir):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"move {remote_file_path} into {remote_dir}")
        self.logger.info("--------------------------------------------------------------------------------")

        self.logger.info(f"execute: mv {remote_file_path} {remote_dir}")
        self.__exec_command(f"mv {remote_file_path} {remote_dir}")


    def ls(self, remote_dir):
        """[summary]

        Parameters
        ----------
        remote_dir : [type]
            [description]

        Returns
        -------
        list
            all items in remote_dir
        """
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"list files in {remote_dir}")
        self.logger.info("--------------------------------------------------------------------------------")

        sftp = self.ssh.open_sftp()

        items = sftp.listdir(remote_dir)
        items.sort()
        for item in items:
            self.logger.info(item)

        sftp.close()

        return items