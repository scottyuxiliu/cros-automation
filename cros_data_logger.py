import os, sys, select, logging, argparse, time
import paramiko

class CrosDataLogger():
    """[summary]
    """

    def __init__(self, test_system_ip_address, test_system_username, ssh_private_key_file, debug):
        self.logger = logging.getLogger("cros_automation.CrosDataLogger")
        fh = logging.FileHandler('cros_data_logger.log', mode='w') # overwrite existing log file
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s') # output method name too
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"establishing ssh connection with the test system ...")
        self.logger.info("--------------------------------------------------------------------------------")

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.logger.info(f"fetch ssh private key file {ssh_private_key_file}")
        ssh_private_key = paramiko.RSAKey.from_private_key_file(ssh_private_key_file)

        self.logger.info(f"connect to test system with the following details")
        self.logger.info(f"hostname = {test_system_ip_address}")
        self.logger.info(f"username = {test_system_username}")
        self.logger.info(f"ssh_private_key_file = {ssh_private_key_file}")

        try:
            self.ssh.connect(hostname=test_system_ip_address, username=test_system_username, pkey=ssh_private_key)
        except paramiko.AuthenticationException:
            self.logger.error(f"paramiko authentication failed when connecting to {test_system_ip_address}. it may be possible to retry with different credentials.")
        except paramiko.SSHException:
            self.logger.error(f"paramiko ssh exception when connecting to {test_system_ip_address}. there might be failures in SSH2 protocol negotiation or logic errors.")

        self.logger.info("ssh session established!")

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
        self.logger.info("test connection to the test system ...")
        self.logger.info("--------------------------------------------------------------------------------")

        status = self.ssh.get_transport().is_active()
        if status is True:
            self.logger.info("ssh session is active")

            self.logger.info('executing echo "ssh session is active"')
            try:
                stdin, stdout, stderr = self.ssh.exec_command('echo "ssh session is active"') # non-blocking call
                self.__read_stdout(stdout)
            except paramiko.SSHException:
                self.logger.error("paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")
        else:
            self.logger.info("ssh session is closed")
        return status


    def launch_atitool_logging(self, duration=60, output_file_name="pm.csv"):
        """[summary]

        Parameters
        ----------
        duration : int, optional
            [description], by default 60
        output_file_name : str, optional
            [description], by default "pm.csv"
        """
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"launching {duration}-second atitool logging on the test system ...")
        self.logger.info("--------------------------------------------------------------------------------")

        self.logger.info(f'executing: cd /usr/local/atitool; ./atitool -i=1 -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput="{output_file_name}"')
        try:
            if self.debug is True:
                stdin, stdout, stderr = self.ssh.exec_command(f'cd /usr/local/atitool; ./atitool -i=1 -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput="{output_file_name}"') # non-blocking call
                self.__read_stdout(stdout)
                self.logger.info("atitool logging finished on the test system")
            else:
                self.ssh.exec_command(f'cd /usr/local/atitool; ./atitool -i=1 -pmlogall -pmcount={duration} -pmperiod=1000 -pmoutput="{output_file_name}"') # non-blocking call
                time.sleep(1) # exec_command does not work properly without this
                self.logger.info("atitool logging started on the test system")
        except paramiko.SSHException:
            self.logger.error("paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")



    def download_file(self, remote_file_path, local_file_path):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"downloading {remote_file_path} to {local_file_path} ...")
        self.logger.info("--------------------------------------------------------------------------------")

        sftp = self.ssh.open_sftp()
        sftp.get(remote_file_path, local_file_path)

        self.logger.info(f"downloaded {local_file_path}")


    def upload_file(self, local_file_path, remote_file_path):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"uploading {local_file_path} to {remote_file_path} ...")
        self.logger.info("--------------------------------------------------------------------------------")

        sftp = self.ssh.open_sftp()
        sftp.put(local_file_path, remote_file_path)

        self.logger.info(f"uploaded {remote_file_path}")

    
    def remove_file(self, remote_file_path):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"removing {remote_file_path} ...")
        self.logger.info("--------------------------------------------------------------------------------")

        sftp = self.ssh.open_sftp()
        try:
            sftp.remove(remote_file_path)
            self.logger.info(f"removed {remote_file_path}")
        except IOError:
            self.logger.error("remote_file_path might be a directory.")


    def ls(self, remote_directory):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"ls {remote_directory} ...")
        self.logger.info("--------------------------------------------------------------------------------")

        sftp = self.ssh.open_sftp()

        items = sftp.listdir(remote_directory)
        items.sort()
        for item in items:
            self.logger.info(item)