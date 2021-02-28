import os, sys, select, logging, time, glob, pathlib
import paramiko

class CrosDataParser():
    """[summary]
    """

    def __init__(self):
        self.logger = logging.getLogger("cros_automation.CrosDataParser")
        fh = logging.FileHandler('cros_data_parser.log', mode='w') # overwrite existing log file
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s') # output method name too
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    
    def __enter__(self):
        return self


    def __exit__(self, exit_type, exit_value, traceback):
        pass


    def __read_path(self, path):
        path.replace("\\", "/")
        return pathlib.Path(path)


    def ls_local(self, directory, name=None):
        if name is None:
            self.logger.info("--------------------------------------------------------------------------------")
            self.logger.info(f"list files in {directory} ...")
            self.logger.info("--------------------------------------------------------------------------------")
        elif name.startswith("*") and name.endswith("*"):
            self.logger.info("--------------------------------------------------------------------------------")
            self.logger.info(f"list files in {directory} that have {name.strip('*')} in their file names ...")
            self.logger.info("--------------------------------------------------------------------------------")
        elif name.startswith("*"):
            self.logger.info("--------------------------------------------------------------------------------")
            self.logger.info(f"list files in {directory} with file names ending with {name.lstrip('*')} ...")
            self.logger.info("--------------------------------------------------------------------------------")
        elif name.endswith("*"):
            self.logger.info("--------------------------------------------------------------------------------")
            self.logger.info(f"list files in {directory} with file names starting with {name.rstrip('*')} ...")
            self.logger.info("--------------------------------------------------------------------------------")
        else:
            self.logger.info("--------------------------------------------------------------------------------")
            self.logger.info(f"list files in {directory} with file names matching {name} ...")
            self.logger.info("--------------------------------------------------------------------------------")