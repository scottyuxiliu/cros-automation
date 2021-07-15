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
    def __read_stdout(self, stdout) -> list:
        """this will be blocking.

        Args:
            stdout ([type]): [description]

        Returns:
            list: [description]
        """

        content = []

        if stdout.channel.recv_exit_status() != 0:
            self.logger.error(f"{'(DEBUG MODE) ' if self.debug else ''}stdout.channel.recv_exit_status() returned {stdout.channel.recv_exit_status()}")

        try:
            for line in stdout.readlines():
                line = line.rstrip("\n")
                self.logger.debug(f"{'(DEBUG MODE) ' if self.debug else ''}{line}")
                content.append(line)
        except UnicodeDecodeError as ude:
            self.logger.error(f"{ude.__class__} stdout has garbage")
            self.logger.error(f"original error message: {ude}")

        return content


    def __exec_command(self, command, read_stdout=False, password=None, verbose=True) -> list:
        """execute command using paramiko ssh.exec_command().

        if self.debug is true or read_stdout is true, this will be blocking and stdout will be read.

        if password is not none, password will be written through stdin.

        Args:
            command (str): [description]
            read_stdout (bool, optional): if true, paramiko ssh.exec_command() will be blocking and stdout will be read. Defaults to False.
            password (str, optional): password to be written through stdin. Defaults to None.
            verbose (bool, optional): output to console if True, suppress output if False. Defaults to True.

        Returns:
            list: stdout from paramiko ssh.exec_command() parsed by self.__read_stdout
            
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
                if verbose is True:
                    self.logger.info("command completed on the DUT")
                else:
                    self.logger.debug("command completed on the DUT")
            else:
                n = len(command.split(";")) # get the number of commands that should be executed
                time.sleep(n) # exec_command does not work properly without this. every additional command requires one more second of wait time.
                if verbose is True:
                    self.logger.info("started on the DUT")
                else:
                    self.logger.debug("started on the DUT")

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
        self.logger.info(f"reboot {self.ip}")
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


    def flashrom(self, apfw):
        """this will be blocking.

        Args:
            apfw (str): path to the apfw
        """

        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"flash apfw {apfw} on {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")

        self.logger.info(f"execute: flashrom -p host -w {apfw}")
        self.__exec_command(f"flashrom -p host -w {apfw}", read_stdout=True)


    # def servo_flashrom(self, apfw, sudo_password):
    #     """this will be blocking.

    #     Parameters
    #     ----------
    #     apfw : [type]
    #         [description]
    #     """
    #     self.logger.info("--------------------------------------------------------------------------------")
    #     self.logger.info(f"use servo on {self.ip} to flash coreboot firmware {apfw}")
    #     self.logger.info("--------------------------------------------------------------------------------")

    #     self.logger.info("sudo execute (blocking): dut-control servo_present:on cold_reset:on spi2_vref:pp1800 spi2_buf_en:on")
    #     self.__exec_command("dut-control servo_present:on cold_reset:on spi2_vref:pp1800 spi2_buf_en:on", sudo_password)

    #     time.sleep(5)

    #     self.logger.info(f"sudo execute (blocking): sudo flashrom --programmer raiden_debug_spi -w {apfw}")
    #     self.__exec_command(f"sudo flashrom --programmer raiden_debug_spi -w {apfw}", sudo_password)

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

        self.logger.info(f"execute: cd /usr/local/agt_internal; ./agt_internal {args}")
        self.__exec_command(f"cd /usr/local/agt_internal; ./agt_internal {args}", True)


    def get_brightness(self):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"get panel brightness on {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"execute: cd /sys/devices/pci0000:00/0000:00:08.1/0000:04:00.0/backlight/amdgpu_bl0; cat brightness")
        stdout = self.__exec_command(f"cd /sys/devices/pci0000:00/0000:00:08.1/0000:04:00.0/backlight/amdgpu_bl0; cat brightness", True)
        for line in stdout:
            self.logger.info(line)


    def set_brightness(self, nit):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"set panel brightness {nit} nits on {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"execute: cd /sys/devices/pci0000:00/0000:00:08.1/0000:04:00.0/backlight/amdgpu_bl0; echo {nit} > brightness")
        self.__exec_command(f"cd /sys/devices/pci0000:00/0000:00:08.1/0000:04:00.0/backlight/amdgpu_bl0; echo {nit} > brightness")


    def get_chrome_os_version(self):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"get chrome os version on {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info("execute: cat /etc/lsb-release")
        stdout = self.__exec_command("cat /etc/lsb-release", True)
        for line in stdout:
            self.logger.info(line)


    def get_coreboot_fw_version(self):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"get apfw version on {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info("execute: crossystem | grep fwid")
        stdout = self.__exec_command("crossystem | grep fwid", True)
        for line in stdout:
            self.logger.info(line)


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


    def __get_offline_cpu_cores(self) -> int:
        core_info = self.__exec_command("cat /sys/devices/system/cpu/offline", read_stdout=True, verbose=False)
        core_info = core_info[0]

        if not core_info:
            self.logger.info("currently cores [] are offline")
            return []

        elif "-" in core_info:
            cores = core_info.split("-")
            core_min = int(cores[0])
            core_max = int(cores[-1])
            self.logger.info(f"currently cores {list(range(core_min, core_max+1))} are offline")
            return range(core_min, core_max+1) # In Python 2.x, range returns a list, but in Python 3.x range returns an immutable sequence, of type range. Since range objects in Python 3 are immutable sequences, they support indexing as well.
        else:
            core_min = int(core_info)
            self.logger.info(f"currently core {[core_min]} is offline")
            return [core_min]

    
    def get_offline_cpu_cores(self) -> int:
        core_info = self.__exec_command("cat /sys/devices/system/cpu/offline", read_stdout=True, verbose=False)
        core_info = core_info[0]

        if not core_info:
            self.logger.info("currently cores [] are offline")
            return []

        elif "-" in core_info:
            cores = core_info.split("-")
            core_min = int(cores[0])
            core_max = int(cores[-1])
            self.logger.info(f"currently cores {list(range(core_min, core_max+1))} are offline")
            return range(core_min, core_max+1) # In Python 2.x, range returns a list, but in Python 3.x range returns an immutable sequence, of type range. Since range objects in Python 3 are immutable sequences, they support indexing as well.
        else:
            core_min = int(core_info)
            self.logger.info(f"currently core {[core_min]} is offline")
            return [core_min]

    def enable_cpu_cores(self, num_cores: int) -> None:
        """

        Parameters
        ----------
        num_cores : int

        Returns
        -------
        object
        """
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"enable {num_cores} cpu cores on {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")
        core_list = self.__get_offline_cpu_cores()
        max_num_cores = len(core_list)

        if num_cores > max_num_cores:
            raise ValueError(f"user tries to enable {num_cores} {'core' if num_cores==1 else 'cores'}, but the maximum allowed {'core' if max_num_cores==1 else 'cores'} {max_num_cores} {'core' if max_num_cores==1 else 'cores'}.")
        else:
            for i in range(num_cores):
                self.logger.info(f"execute: echo 1 > /sys/devices/system/cpu/cpu{core_list[i]}/online")
                self.__exec_command(f"echo 1 > /sys/devices/system/cpu/cpu{core_list[i]}/online", read_stdout=True)

    def __get_online_cpu_cores(self) -> list:
        """

        Returns
        -------
        list

        """
        core_info = self.__exec_command("cat /sys/devices/system/cpu/online", read_stdout=True, verbose=False)
        core_info = core_info[0]

        if "-" in core_info:
            cores = core_info.split("-")
            core_min = int(cores[0])
            core_max = int(cores[-1])
            self.logger.info(f"currently cores {list(range(core_max, core_min-1, -1))} are online")
            return range(core_max, core_min-1, -1)
        else:
            core_max = int(core_info)
            self.logger.info(f"currently core {[core_max]} is online")
            return [core_max]

    def get_online_cpu_cores(self) -> None:
        """

        """
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"get list of online cpu cores on {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")
        core_info = self.__exec_command("cat /sys/devices/system/cpu/online", read_stdout=True, verbose=False)
        core_info = core_info[0]

        cores = []
        if "," in core_info:
            for group in core_info.split(","):  # online cores in comma-delimited groups, for example, 0-3, 5
                if "-" in group:
                    group_min = int(group.split("-")[0])
                    group_max = int(group.split("-")[-1])
                    cores.extend([*range(group_min, group_max+1)])  # unpack range to list and add to cores
                else:  # there's only one number in the group
                    cores.append(int(group))

            cores.sort(reverse=True)  # sort in descending order
            self.logger.info(f"currently cores {cores} are online")
        else:
            if "-" in core_info:
                core_min = int(core_info.split("-")[0])
                core_max = int(core_info.split("-")[-1])
                cores.extend([*range(core_max, core_min-1, -1)])
                self.logger.info(f"currently cores {cores} are online")
            else:
                self.logger.info(f"currently core {int(core_info)} is online")

    def disable_cpu_cores(self, num_cores: int) -> None:
        """[summary]

        Parameters
        ----------
        num_cores : int
            [description]

        Raises
        ------
        ValueError
            [description]
        """
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"disable {num_cores} cpu cores on {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")
        core_list = self.__get_online_cpu_cores()
        max_num_cores = len(core_list) - 1 # can not disable core 0

        if num_cores > max_num_cores:
            raise ValueError(
                f"user tries to disable {num_cores} {'core' if num_cores==1 else 'cores'}, "
                f"but the maximum allowed {'is' if max_num_cores==1 else 'are'}"
                f"{max_num_cores} {'core' if max_num_cores==1 else 'cores'}. "
                f"note that core 0 can not be disabled."
            )
        else:
            for i in range(num_cores):
                self.logger.info(f"execute: echo 0 > /sys/devices/system/cpu/cpu{core_list[i]}/online")
                self.__exec_command(f"echo 0 > /sys/devices/system/cpu/cpu{max_num_cores-i}/online", read_stdout=True)

    def disable_hyper_threading(self) -> None:
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"disable hyper threading on {self.ip}")
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"execute: /usr/libexec/debugd/helpers/scheduler_configuration_helper --policy=conservative")
        self.__exec_command("/usr/libexec/debugd/helpers/scheduler_configuration_helper --policy=conservative")
