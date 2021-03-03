import os, sys, select, logging, time, errno, pathlib, stat
import paramiko

class CrosDataLogger():
    """[summary]
    """

    def __init__(self, test_system_ip_address, test_system_username, ssh_private_key_file, debug):
        self.logger = logging.getLogger("cros_automation.CrosDataLogger")
        fh = logging.FileHandler("cros_data_logger.log", mode="w") # overwrite existing log file
        # fh = logging.FileHandler("cros_data_logger.log")
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
        # except paramiko.AuthenticationException:
        #     self.logger.error(f"paramiko authentication failed when connecting to {test_system_ip_address}. it may be possible to retry with different credentials.")
        # except paramiko.SSHException:
        #     self.logger.error(f"paramiko ssh exception when connecting to {test_system_ip_address}. there might be failures in SSH2 protocol negotiation or logic errors.")

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

        
    def __exist(self, path):
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
                self.logger.error("paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")
        else:
            self.logger.info("ssh session is closed")
        return status


    def launch_atitool_logging(self, duration, index, output_file_name="pm.csv"):
        """atitool path should be /usr/local/atitool

        Parameters
        ----------
        duration : int, optional
            [description], by default 60
        output_file_name : str, optional
            [description], by default "pm.csv"
        """
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"launch {duration}-second atitool logging on the test system {self.test_system_ip_address} ...")
        self.logger.info("--------------------------------------------------------------------------------")

        if index == 0:
            self.logger.info(f'executing: cd /usr/local/atitool; ./atitool -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput="{output_file_name}"')
        else:
            self.logger.info(f'executing: cd /usr/local/atitool; ./atitool -i={index} -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput="{output_file_name}"')

        try:
            if self.debug is True:
                if index == 0:
                    stdin, stdout, stderr = self.ssh.exec_command(f'cd /usr/local/atitool; ./atitool -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput="{output_file_name}"') # non-blocking call
                else:
                    stdin, stdout, stderr = self.ssh.exec_command(f'cd /usr/local/atitool; ./atitool -i={index} -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput="{output_file_name}"') # non-blocking call

                self.__read_stdout(stdout)
                self.logger.info("atitool logging finished on the test system")
            else:
                if index == 0:
                    self.ssh.exec_command(f'cd /usr/local/atitool; ./atitool -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput="{output_file_name}"') # non-blocking call
                else:
                    self.ssh.exec_command(f'cd /usr/local/atitool; ./atitool -i={index} -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput="{output_file_name}"') # non-blocking call

                time.sleep(1) # exec_command does not work properly without this
                self.logger.info("atitool logging started on the test system")
        except paramiko.SSHException:
            self.logger.error("paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")


    def is_file(self, path):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"check if {path} is a file or a directory ...")
        self.logger.info("--------------------------------------------------------------------------------")

        path = str( self.__read_path(path) )

        if self.__exist(path):
            self.logger.info(f"{path} exists")
            # sftp = self.ssh.open_sftp()
            # for fileattr in sftp.listdir_attr(path):
            #     if stat.S_ISDIR(fileattr.st_mode):
            #         self.logger.info("it is a directory")
            #         return False
            #     else:
            #         self.logger.info("it is a file")
            #         return True
        else:
            self.logger.info(f"no such file or directory: {path}")


    def download_file(self, remote_file_path, local_file_path):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"download {remote_file_path} to {local_file_path} ...")
        self.logger.info("--------------------------------------------------------------------------------")

        sftp = self.ssh.open_sftp()
        sftp.get(remote_file_path, local_file_path)

        self.logger.info(f"downloaded {local_file_path}")
        sftp.close()


    def upload_file(self, local_file_path, remote_file_path):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"upload {local_file_path} to {remote_file_path} ...")
        self.logger.info("--------------------------------------------------------------------------------")

        if self.__exist(remote_file_path):
            self.logger.info(f"{remote_file_path} already exists")
        else:
            sftp = self.ssh.open_sftp()
            sftp.put(local_file_path, remote_file_path)
            self.logger.info(f"uploaded {remote_file_path}")
            sftp.close()

    
    def remove_file(self, remote_file_path):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"remove {remote_file_path} ...")
        self.logger.info("--------------------------------------------------------------------------------")

        sftp = self.ssh.open_sftp()
        try:
            sftp.remove(remote_file_path)
        except IOError:
            self.logger.error("remote_file_path might be a directory.")
        else:
            self.logger.info(f"removed {remote_file_path}")

        sftp.close()


    def extract_file(self, remote_file_path):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"extract {remote_file_path} ...")
        self.logger.info("--------------------------------------------------------------------------------")

        if self.__exist(remote_file_path):
            p = self.__read_path(remote_file_path)
            directory = str(p.parent)
            filename = p.name

            self.logger.info(f"executing: cd {directory}; tar -xzvf {filename}")

            try:
                if self.debug is True:
                    stdin, stdout, stderr = self.ssh.exec_command(f"cd {directory}; tar -xzvf {filename}") # non-blocking call
                    self.__read_stdout(stdout)
                    self.logger.info("file extraction finished on the test system")
                else:
                    self.ssh.exec_command(f"cd {directory}; tar -xzvf {filename}") # non-blocking call
                    time.sleep(1) # exec_command does not work properly without this
                    self.logger.info("file extraction started on the test system")
            except paramiko.SSHException:
                self.logger.error("paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")

        else:
            self.logger.error(f"no such file: {remote_file_path}")


    def mkdir(self, remote_dir):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"create directory {remote_dir} ...")
        self.logger.info("--------------------------------------------------------------------------------")

        if self.__exist(remote_dir):
            self.logger.info(f"{remote_dir} already exists")
        else:
            sftp = self.ssh.open_sftp()
            sftp.mkdir(remote_dir)
            self.logger.info(f"{remote_dir} created")
            sftp.close()


    def rmdir(self, remote_dir):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"remove directory {remote_dir} ...")
        self.logger.info("--------------------------------------------------------------------------------")

        if self.__exist(remote_dir):
            if self.debug is True:
                try:
                    stdin, stdout, stderr = self.ssh.exec_command(f"rm -r {remote_dir}") # non-blocking call
                    self.__read_stdout(stdout)
                except paramiko.SSHException:
                    self.logger.error("paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")
                else:
                    self.logger.info(f"removed {remote_dir} on the test system")
            else:
                try:
                    self.ssh.exec_command(f"rm -r {remote_dir}") # non-blocking call
                except paramiko.SSHException:
                    self.logger.error("paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")
                else:
                    self.logger.info(f"started to remove {remote_dir} on the test system")
        else:
            self.logger.error(f"no such directory: {remote_dir}")


    def ls(self, remote_dir):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"list files in {remote_dir} ...")
        self.logger.info("--------------------------------------------------------------------------------")

        sftp = self.ssh.open_sftp()

        items = sftp.listdir(remote_dir)
        items.sort()
        for item in items:
            self.logger.info(item)

        sftp.close()