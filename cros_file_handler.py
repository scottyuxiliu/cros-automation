import os, sys, select, logging, argparse, time, errno, pathlib, stat
import paramiko

class CrosFileHandler():
    """set debug to True to enable debug mode
    """

    def __init__(self, ip, username, ssh_private_key_file, debug) -> None:
        """[summary]

        Parameters
        ----------
        ip : [type]
            [description]
        username : [type]
            [description]
        ssh_private_key_file : [type]
            [description]
        debug : [type]
            [description]
        """

        self.logger = logging.getLogger("cros_automation.CrosFileHandler")
        fh = logging.FileHandler("cros_file_handler.log") # to overwrite existing log file, use mode="w"
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s') # output method name too
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        self.logger.debug("--------------------------------------------------------------------------------")
        self.logger.debug(f"establish ssh connection with the host system")
        self.logger.debug("--------------------------------------------------------------------------------")

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.logger.debug(f"fetch ssh private key file {ssh_private_key_file}")
        ssh_private_key = paramiko.RSAKey.from_private_key_file(ssh_private_key_file)

        self.logger.debug(f"connect to test system with the following details")
        self.logger.debug(f"hostname = {ip}")
        self.logger.debug(f"username = {username}")
        self.logger.debug(f"ssh_private_key_file = {ssh_private_key_file}")

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


    def __is_file(self, path):
        sftp = self.ssh.open_sftp()
        if stat.S_ISDIR( sftp.stat(path).st_mode ):
            # self.logger.info(f"{path} is a directory.")
            return False
        else:
            # self.logger.info(f"{path} is a file.")
            return True


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
        self.logger.info(f"ls {remote_dir} on {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")

        if remote_dir is None:
            raise ValueError("remote_dir is none!")
        
        sftp = self.ssh.open_sftp()

        items = sftp.listdir(remote_dir)
        items.sort()
        for item in items:
            self.logger.info(item)

        sftp.close()

        return items


    def mkdir(self, remote_dir):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"create directory {remote_dir}")
        self.logger.info("--------------------------------------------------------------------------------")

        if self.__exist_remote(remote_dir):
            self.logger.info(f"{remote_dir} already exists")
        else:
            sftp = self.ssh.open_sftp()
            sftp.mkdir(remote_dir)
            self.logger.info(f"{remote_dir} created")
            sftp.close()


    def rm(self, remote_file_path):
        """this will be blocking.

        Parameters
        ----------
        remote_file_path : str
            [description]
        """
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"rm {remote_file_path} on {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")

        if remote_file_path is None:
            raise ValueError("remote_file_path is none!")
        
        if self.__exist_remote(remote_file_path):
            sftp = self.ssh.open_sftp()
            try:
                sftp.remove(remote_file_path)
            except IOError:
                self.logger.error("remote_file_path might be a directory!")
            else:
                self.logger.info(f"removed {remote_file_path}")

            sftp.close()
        else:
            self.logger.error(f"no such file: {remote_file_path}")


    def rmdir(self, remote_dir):
        """this will be blocking.

        Parameters
        ----------
        remote_dir : [type]
            [description]

        Raises
        ------
        ValueError
            [description]
        """
        
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"rmdir {remote_dir} on {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")

        if remote_dir is None:
            raise ValueError("remote_dir is none!")

        # path = str( self.__read_path(path) )

        if self.__exist_remote(remote_dir):
            if self.__is_file(remote_dir) is False:
                self.logger.info(f"execute: rm -r {remote_dir}")
                self.__exec_command(f"rm -r {remote_dir}", read_stdout=True)
            else:
                self.logger.error(f"{remote_dir} is file. run rm instead.")
        else:
            self.logger.error(f"no such directory: {remote_dir}")


    def __download_progress(self, current, total):
        self.logger.debug(f"downloaded {current} bytes / {total} bytes")


    def download(self, remote_file_path, local_file_path):
        """[summary]

        Parameters
        ----------
        remote_file_path : str
            remote file path, for example, "/usr/local/test"
        local_file_path : str
            local file path, for example, "C:/Users/scottyuxiliu/Downloads/test"
        """

        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"download {remote_file_path} to {local_file_path}")
        self.logger.info("--------------------------------------------------------------------------------")

        if remote_file_path is None:
            raise ValueError("remote_file_path is none!")
        
        if local_file_path is None:
            raise ValueError("local_file_path is none!")

        if self.__exist_remote(remote_file_path):
            sftp = self.ssh.open_sftp()
            sftp.get(remote_file_path, local_file_path, callback=self.__download_progress)
            self.logger.info(f"downloaded {local_file_path}")
            sftp.close()
        else:
            self.logger.error(f"no such file: {remote_file_path}")


    def __upload_progress(self, current, total):
        self.logger.debug(f"uploaded {current} bytes / {total} bytes")
    

    def upload(self, local_file_path, remote_file_path):
        """this will be blocking.

        Parameters
        ----------
        local_file_path : str
            local file path, for example, "C:/Users/scottyuxiliu/Downloads/test"
        remote_file_path : str
            remote file path, for example, "/usr/local/test"
        """

        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"upload {local_file_path} to {remote_file_path}")
        self.logger.info("--------------------------------------------------------------------------------")
        sftp = self.ssh.open_sftp()
        sftp.put(local_file_path, remote_file_path, callback=self.__upload_progress)
        sftp.close()
        self.logger.info(f"uploaded {remote_file_path}")


    def extract(self, remote_file_path):
        """this will be blocking.

        Parameters
        ----------
        remote_file_path : [type]
            [description]

        Raises
        ------
        ValueError
            [description]
        """
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"extract {remote_file_path}")
        self.logger.info("--------------------------------------------------------------------------------")

        if remote_file_path is None:
            raise ValueError("remote_file_path is none!")

        if self.__exist_remote(remote_file_path):
            p = self.__read_path(remote_file_path, True)
            directory = str(p.parent)
            filename = p.name

            self.logger.info(f"execute: cd {directory}; tar -xzvf {filename}")
            self.__exec_command(f"cd {directory}; tar -xzvf {filename}", read_stdout=True)

        else:
            self.logger.error(f"no such file: {remote_file_path}")


    def compress(self, remote_file_path):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"compress {remote_file_path}")
        self.logger.info("--------------------------------------------------------------------------------")

        if remote_file_path is None:
            raise ValueError("remote_file_path is none!")

        if self.__exist_remote(remote_file_path):
            p = self.__read_path(remote_file_path, True)
            directory = str(p.parent)
            filename = p.name

            self.logger.info(f"execute: cd {directory}; tar -czvf {filename}.tar.gz {filename}")
            self.__exec_command(f"cd {directory}; tar -czvf {filename}.tar.gz {filename}", read_stdout=True)

        else:
            self.logger.error(f"no such file: {remote_file_path}")
    