import os, sys, select, logging, argparse, time, errno, pathlib
import paramiko

from cros_constants import PERL_DIR_PATH

class CrosSwCtrl():
    """[summary]
    """

    def __init__(self, test_system_ip_address, test_system_username, ssh_private_key_file, debug):
        self.logger = logging.getLogger("cros_automation.CrosSwCtrl")
        fh = logging.FileHandler("cros_hw_ctrl.log", mode="w") # overwrite existing log file
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s') # output method name too
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        self.logger.debug("--------------------------------------------------------------------------------")
        self.logger.debug(f"establishing ssh connection with the host system ...")
        self.logger.debug("--------------------------------------------------------------------------------")

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.logger.debug(f"fetch ssh private key file {ssh_private_key_file}")
        ssh_private_key = paramiko.RSAKey.from_private_key_file(ssh_private_key_file)

        self.logger.debug(f"connect to test system with the following details")
        self.logger.debug(f"hostname = {test_system_ip_address}")
        self.logger.debug(f"username = {test_system_username}")
        self.logger.debug(f"ssh_private_key_file = {ssh_private_key_file}")

        self.ssh.connect(hostname=test_system_ip_address, username=test_system_username, pkey=ssh_private_key)
        self.logger.debug("ssh session established!")

        self.test_system_ip_address = test_system_ip_address
        self.debug = debug


    def __enter__(self):
        return self


    def __exit__(self, exit_type, exit_value, traceback):
        self.ssh.close()


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


    def __upload(self, local_file_path, remote_file_path):
        """[summary]

        Parameters
        ----------
        local_file_path : [type]
            [description]
        remote_file_path : [type]
            [description]
        """
        sftp = self.ssh.open_sftp()
        sftp.put(local_file_path, remote_file_path)
        sftp.close()


    def install_perl(self, perl_path):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"install perl on the test system {self.test_system_ip_address} ...")
        self.logger.info("--------------------------------------------------------------------------------")

        self.logger.info("")
        self.logger.info(f"upload {perl_path} to {PERL_DIR_PATH}")