import os, sys, select, logging, time, glob, pathlib
import paramiko
import pandas as pd

class CrosDataParser():
    """[summary]
    """

    def __init__(self):
        self.logger = logging.getLogger("cros_automation.CrosDataParser")
        fh = logging.FileHandler("cros_data_parser.log", mode="w") # overwrite existing log file
        # fh = logging.FileHandler("cros_data_parser.log")
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(funcName)s - %(message)s') # output method name too
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    
    def __enter__(self):
        return self


    def __exit__(self, exit_type, exit_value, traceback):
        pass


    def __read_path(self, path):
        """read path in string format and convert it to pathlib.Path() object

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
        return pathlib.Path(path)


    def ls_local(self, directory, name=None):
        if name is None:
            self.logger.info("--------------------------------------------------------------------------------")
            self.logger.info(f"list files in {directory} ...")
            self.logger.info("--------------------------------------------------------------------------------")

            name = "*"

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

        directory = self.__read_path(directory)
        items = glob.glob( str(directory.joinpath(name)) )
        if not items:
            self.logger.info("(na)")
        else:
            for item in items:
                self.logger.info(item)

        return items


    def keyvals_to_csv(self, keyvals):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"convert keyvals to .csv files ...")
        self.logger.info("--------------------------------------------------------------------------------")

        for keyval in keyvals:
            content_dict = {}

            with open(keyval, "r") as f:
                for line in f.readlines(): # f.readlines() will point to the end of file after finish
                    line_items = line.split("=")
                    self.logger.debug(line_items)
                    content_dict[ line_items[0].strip() ] =  line_items[-1].strip()

            content_df = pd.DataFrame.from_records( [content_dict] )
            self.logger.info(f"{keyval} content:\n{content_df}")

            content_df.to_csv(f"{keyval}.csv", index=False)
