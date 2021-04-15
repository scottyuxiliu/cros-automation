import os, sys, select, logging, argparse, time, errno, pathlib
import paramiko

import cros_constants

class CrosSoftwareController():
    """[summary]
    """

    def __init__(self, ip, username, ssh_private_key_file, debug):
        self.logger = logging.getLogger("cros_automation.CrosSoftwareController")
        fh = logging.FileHandler("cros_software_controller.log") # to overwrite existing log file, use mode="w"
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
        content = []

        if stdout.channel.recv_exit_status() == 0: # blocking call
            self.logger.debug("****************************** stdout content ******************************")
            for line in stdout.readlines():
                self.logger.debug(line)
                content.append(line)
        else:
            self.logger.error(f"stdout.channel.recv_exit_status() returned {stdout.channel.recv_exit_status()}")
            self.logger.error("****************************** stdout content ******************************")
            for line in stdout.readlines():
                self.logger.error(line)
                content.append(line)

        return content


    def __exec_command(self, command, sudo_password=None, blocking=False):
        """execute command using paramiko ssh.exec_command()

        if sudo_password is provided, command will be executed with su privileges. this will be blocking.

        Parameters
        ----------
        command : str
            [description]
        sudo_password : str
            [description]
        blocking : bool
            if set, paramiko ssh.exec_command() will be blocking.
        """

        if sudo_password is not None:
            stdout = None

            try:
                stdin, stdout, stderr = self.ssh.exec_command(f"sudo -S -p '' {command}") # non-blocking call
                stdin.write(f"{sudo_password}\n")
                stdin.flush()
                stdout = self.__read_stdout(stdout)
            except paramiko.SSHException:
                self.logger.error("paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")
            else:
                self.logger.info("finished on the test system with su privileges")

            return stdout # need to return after the try/except/else blocks. python will not go inside the else block if a value is returned in the try block.
        else:
            if self.debug is True or blocking is True:
                stdout = None

                try:
                    stdin, stdout, stderr = self.ssh.exec_command(command) # non-blocking call
                    stdout = self.__read_stdout(stdout) # if debug flag is set, capture stdout from exec_command
                except paramiko.SSHException:
                    self.logger.error("paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")
                else:
                    self.logger.info("finished on the test system")

                return stdout # need to return after the try/except/else blocks. python will not go inside the else block if a value is returned in the try block.
            else:
                n = len(command.split(";")) # get the number of commands that should be executed

                try:
                    self.ssh.exec_command(command) # non-blocking call, thus need to add delay after
                except paramiko.SSHException:
                    self.logger.error("paramiko ssh exception. there might be failures in SSH2 protocol negotiation or logic errors.")
                else:
                    time.sleep(n) # exec_command does not work properly without this. every additional command requires one more second of wait time.
                    self.logger.info("started on the test system")


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


    def reboot(self):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"reboot the target system {self.ip} ...")
        self.logger.info("--------------------------------------------------------------------------------")

        self.logger.info("execute: /sbin/reboot -f > /dev/null 2>&1 &")
        self.__exec_command("/sbin/reboot -f > /dev/null 2>&1 &")


    def cold_reset(self, sudo_password):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info("start servo cold-reset ...")
        self.logger.info("--------------------------------------------------------------------------------")

        self.logger.info("sudo execute (blocking): dut-control servo_present:on cold_reset:on spi2_vref:pp1800 spi2_buf_en:on")
        self.__exec_command("dut-control servo_present:on cold_reset:on spi2_vref:pp1800 spi2_buf_en:on", sudo_password)

        self.logger.info("wait 10 seconds")
        time.sleep(10)

        self.logger.info("sudo execute (blocking): dut-control spi2_vref:off spi2_buf_en:off cold_reset:off servo_present:off")
        self.__exec_command("dut-control spi2_vref:off spi2_buf_en:off cold_reset:off servo_present:off", sudo_password)


    def flashrom(self, coreboot_firmware):
        """this will be blocking.

        Parameters
        ----------
        coreboot_firmware : [type]
            [description]
        """
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"flash coreboot firmware {coreboot_firmware} on {self.ip} ...")
        self.logger.info("--------------------------------------------------------------------------------")

        self.logger.info(f"execute (blocking): flashrom -p host -w {coreboot_firmware}")
        self.__exec_command(f"flashrom -p host -w {coreboot_firmware}", blocking=True)


    def servo_flashrom(self, coreboot_firmware, sudo_password):
        """this will be blocking.

        Parameters
        ----------
        coreboot_firmware : [type]
            [description]
        """
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"use servo on {self.ip} to flash coreboot firmware {coreboot_firmware} ...")
        self.logger.info("--------------------------------------------------------------------------------")

        self.logger.info("sudo execute (blocking): dut-control servo_present:on cold_reset:on spi2_vref:pp1800 spi2_buf_en:on")
        self.__exec_command("dut-control servo_present:on cold_reset:on spi2_vref:pp1800 spi2_buf_en:on", sudo_password)

        time.sleep(5)

        self.logger.info(f"sudo execute (blocking): sudo flashrom --programmer raiden_debug_spi -w {coreboot_firmware}")
        self.__exec_command(f"sudo flashrom --programmer raiden_debug_spi -w {coreboot_firmware}", sudo_password)

        time.sleep(5)

        self.logger.info("sudo execute (blocking): dut-control spi2_vref:off spi2_buf_en:off cold_reset:off servo_present:off")
        self.__exec_command("dut-control spi2_vref:off spi2_buf_en:off cold_reset:off servo_present:off", sudo_password)


    def agt_prog(self, args):
        """this will be blocking.

        Parameters
        ----------
        args : [type]
            [description]
        """
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"agt program {args} ...")
        self.logger.info("--------------------------------------------------------------------------------")

        self.logger.info(f"execute (blocking): cd /usr/local/agt; ./agt_internal {args}")
        self.__exec_command(f"cd /usr/local/agt; ./agt_internal {args}", blocking=True)

    