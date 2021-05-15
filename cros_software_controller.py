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


    def __exec_command(self, command, read_stdout=False, password=None):
        """execute command using paramiko ssh.exec_command().

        if self.debug is true or read_stdout is true, this will be blocking and stdout will be read.

        if password is not none, password will be written through stdin.

        Args:
            command (str): [description]
            read_stdout (bool, optional): if true, paramiko ssh.exec_command() will be blocking and stdout will be read. Defaults to False.
            password (str, optional): password to be written through stdin. Defaults to None.

        Returns:
            [type]: [description]
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
                stdout = self.__read_stdout(stdout) # if debug flag is true or read_stdout is true, capture stdout from exec_command
            else:
                n = len(command.split(";")) # get the number of commands that should be executed
                time.sleep(n) # exec_command does not work properly without this. every additional command requires one more second of wait time.
                self.logger.info("started on the test system")

        return stdout # need to return after the try/except/else blocks. python will not go inside the else block if a value is returned in the try block.


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
        self.logger.info(f"reboot the target system {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")

        self.logger.info("execute: /sbin/reboot -f > /dev/null 2>&1 &")
        self.__exec_command("/sbin/reboot -f > /dev/null 2>&1 &")


    def cold_reset(self, password):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info("start servo cold-reset")
        self.logger.info("--------------------------------------------------------------------------------")

        self.logger.info("execute: sudo -S -p '' \"dut-control servo_present:on cold_reset:on spi2_vref:pp1800 spi2_buf_en:on\"")
        self.__exec_command("sudo -S -p '' \"dut-control servo_present:on cold_reset:on spi2_vref:pp1800 spi2_buf_en:on\"", True, password)

        self.logger.info("wait 10 seconds")
        time.sleep(10)

        self.logger.info("execute: sudo -S -p '' \"dut-control spi2_vref:off spi2_buf_en:off cold_reset:off servo_present:off\"")
        self.__exec_command("sudo -S -p '' \"dut-control spi2_vref:off spi2_buf_en:off cold_reset:off servo_present:off\"", True, password)


    def flashrom(self, coreboot_firmware):
        """this will be blocking.

        Args:
            coreboot_firmware (str): path to the coreboot firmware file
        """

        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"flash coreboot firmware {coreboot_firmware} on {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")

        self.logger.info(f"execute: flashrom -p host -w {coreboot_firmware}")
        self.__exec_command(f"flashrom -p host -w {coreboot_firmware}", True)


    # def servo_flashrom(self, coreboot_firmware, sudo_password):
    #     """this will be blocking.

    #     Parameters
    #     ----------
    #     coreboot_firmware : [type]
    #         [description]
    #     """
    #     self.logger.info("--------------------------------------------------------------------------------")
    #     self.logger.info(f"use servo on {self.ip} to flash coreboot firmware {coreboot_firmware}")
    #     self.logger.info("--------------------------------------------------------------------------------")

    #     self.logger.info("sudo execute (blocking): dut-control servo_present:on cold_reset:on spi2_vref:pp1800 spi2_buf_en:on")
    #     self.__exec_command("dut-control servo_present:on cold_reset:on spi2_vref:pp1800 spi2_buf_en:on", sudo_password)

    #     time.sleep(5)

    #     self.logger.info(f"sudo execute (blocking): sudo flashrom --programmer raiden_debug_spi -w {coreboot_firmware}")
    #     self.__exec_command(f"sudo flashrom --programmer raiden_debug_spi -w {coreboot_firmware}", sudo_password)

    #     time.sleep(5)

    #     self.logger.info("sudo execute (blocking): dut-control spi2_vref:off spi2_buf_en:off cold_reset:off servo_present:off")
    #     self.__exec_command("dut-control spi2_vref:off spi2_buf_en:off cold_reset:off servo_present:off", sudo_password)


    def agt_prog(self, args):
        """this will be blocking.

        Parameters
        ----------
        args : [type]
            [description]
        """
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"agt program {args}")
        self.logger.info("--------------------------------------------------------------------------------")

        self.logger.info(f"execute: cd /usr/local/agt; ./agt_internal {args}")
        self.__exec_command(f"cd /usr/local/agt; ./agt_internal {args}", True)


    def get_brightness(self):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"get panel brightness on {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"execute: cd /sys/devices/pci0000:00/0000:00:08.1/0000:03:00.0/backlight/amdgpu_bl0; cat brightness")
        stdout = self.__exec_command(f"cd /sys/devices/pci0000:00/0000:00:08.1/0000:03:00.0/backlight/amdgpu_bl0; cat brightness", True)
        for line in stdout:
            self.logger.info(line)


    def set_brightness(self, nit):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"set panel brightness {nit} nits on {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"execute: cd /sys/devices/pci0000:00/0000:00:08.1/0000:03:00.0/backlight/amdgpu_bl0; echo {nit} > brightness")
        self.__exec_command(f"cd /sys/devices/pci0000:00/0000:00:08.1/0000:03:00.0/backlight/amdgpu_bl0; echo {nit} > brightness")


    def get_power_supply_info(self):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"get power supply info on {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"execute: power_supply_info")
        stdout = self.__exec_command("power_supply_info", True)
        for line in stdout:
            self.logger.info(line)


    def enable_ac(self):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"enable ac on {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"execute: ectool usbpd 0 auto")
        self.__exec_command(f"ectool usbpd 0 auto")


    def disable_ac(self):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"disable ac on {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"execute: ectool usbpd 0 source")
        self.__exec_command(f"ectool usbpd 0 source")

    