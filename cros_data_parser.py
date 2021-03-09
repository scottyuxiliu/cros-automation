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


    def __read_keyval_file(self, keyval_path):
        content = {}

        self.logger.info(f"reading {keyval_path}")
        with open(keyval_path, "r") as f:
            for line in f.readlines(): # f.readlines() will point to the end of file after finish
                if line.strip():
                    line_items = line.split("=")
                    content[ line_items[0].strip() ] =  line_items[-1].strip()

        return content


    def ls_local(self, directory, name=None):
        """list all files in the local directory. if name is specified, list all files with that name.

        Parameters
        ----------
        directory : [type]
            [description]
        name : [type], optional
            [description], by default None

        Returns
        -------
        list of strings
            a list of all file paths. if name is specified, a possibly-empty list of paths of files with that name.
        """
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


    def keyvals_to_csv(self, keyval_paths):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info("convert keyval files to .csv files ...")
        self.logger.info("--------------------------------------------------------------------------------")

        for keyval_path in keyval_paths:
            content_dict = self.__read_keyval_file(keyval_path)
            content_df = pd.DataFrame.from_records( [content_dict] )
            self.logger.info(f"{keyval_path} content:\n{content_df}")

            content_df.to_csv(f"{keyval_path}.csv", index=False)


    def keyvals_summary(self, keyval_paths, summary_path):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info("summarize keyval file contents to a .csv file ...")
        self.logger.info("--------------------------------------------------------------------------------")

        dictlist = []
        for keyval_path in keyval_paths:
            content_dict = self.__read_keyval_file(keyval_path)
            content_dict["name"] = self.__read_path(keyval_path).name # add file name to content_dict
            self.logger.debug(f"{keyval_path} content: {content_dict}")
            dictlist.append(content_dict)

        content_df = pd.DataFrame(dictlist)
        content_df.to_csv(summary_path, index=False)

