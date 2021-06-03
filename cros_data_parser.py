import os, sys, select, logging, time, glob, pathlib, json, functools, re
import paramiko
import pandas as pd

from cros_constants import AGT_COLS

class CrosDataParser():
    """[summary]
    """

    def __init__(self):
        self.logger = logging.getLogger("cros_automation.CrosDataParser")
        fh = logging.FileHandler("cros_data_parser.log") # to overwrite existing log file, use mode="w"
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


    def __exist_local(self, path):
        p = self.__read_path(path)

        if p.is_file() or p.is_dir():
            return True
        else:
            return False


    def __read_keyval_file(self, keyval_path):
        content = {}

        self.logger.info(f"reading {keyval_path}")
        with open(keyval_path, "r") as f:
            for line in f.readlines(): # f.readlines() will point to the end of file after finish
                if line.strip():
                    line_items = line.split("=")
                    content[ line_items[0].strip() ] =  line_items[-1].strip()

        return content


    def __read_json_file(self, path):
        content = {}

        self.logger.info(f"reading {path}")
        with open(path, "r") as f:
            content = json.load(f)

        return content


    def __merge_df_list(self, df_list, key_column, merge_method):
        """merge dataframe list and returns df. supported merge_method values are "left", "right", "outer", "inner".

        Parameters
        ----------
        df_list : df list
            [description]
        key_column : str
            the column name that will be used as the key during join
        merge_method : str
            supported values are "left", "right", "outer", "inner"

        Returns
        -------
        df
            [description]
        """

        df = functools.reduce(lambda left, right: pd.merge(left, right, how=merge_method, on=key_column), df_list) # joining df list
        # self.logger.debug(f"\nmerged df ({type(df)})\n{df}")

        return df


    def __concat_df_list(self, df_list):
        """concat dataframe list and returns df.

        Parameters
        ----------
        df_list : df list
            [description]

        Returns
        -------
        df
            [description]
        """

        return pd.concat(df_list, ignore_index=True)


    def __filter_csv_cols(self, df, cols):
        return df[cols]


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
            self.logger.info(f"ls {directory}")
            self.logger.info("--------------------------------------------------------------------------------")
            name = "*"
        else:
            self.logger.info("--------------------------------------------------------------------------------")
            self.logger.info(f"ls {directory} with pattern matching {name}")
            self.logger.info("--------------------------------------------------------------------------------")

        if self.__exist_local(directory):
            directory = self.__read_path(directory)
            items = glob.glob( str(directory.joinpath(name)) )
            if not items:
                self.logger.info("(na)")
            else:
                for item in items:
                    self.logger.info(item)

            return items
        else:
            self.logger.error(f"no such directory: {directory}")


    def keyvals_to_csv(self, keyval_paths):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info("convert keyval files to .csv files")
        self.logger.info("--------------------------------------------------------------------------------")

        for keyval_path in keyval_paths:
            content_dict = self.__read_keyval_file(keyval_path)
            content_df = pd.DataFrame.from_records( [content_dict] )
            self.logger.info(f"{keyval_path} content:\n{content_df}")

            content_df.to_csv(f"{keyval_path}.csv", index=False)


    def keyvals_summary(self, keyval_paths, summary_path):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info("summarize keyval files to a .csv file")
        self.logger.info("--------------------------------------------------------------------------------")

        dictlist = []
        for keyval_path in keyval_paths:
            content_dict = self.__read_keyval_file(keyval_path)
            content_dict["name"] = self.__read_path(keyval_path).name # add file name to content_dict
            self.logger.debug(f"{keyval_path} content: {content_dict}")
            dictlist.append(content_dict)

        content_df = pd.DataFrame(dictlist)
        content_df.to_csv(summary_path, index=False)


    def results_charts_summary(self, results_chart_paths, summary_path):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info("summarize results-chart.json files to a .csv file")
        self.logger.info("--------------------------------------------------------------------------------")

        df_list = []
        for results_chart_path in results_chart_paths:
            content_dict = self.__read_json_file(results_chart_path)
            content_dict["name"] = self.__read_path(results_chart_path).name # add file name to content_dict
            content_df = pd.json_normalize(content_dict)
            # self.logger.debug(f"{results_chart_path} content: {content_df}")

            df_list.append(content_df)

        df = self.__concat_df_list(df_list)
        # self.logger.debug(df)
        df.to_csv(summary_path, index=False)


    def agt_cols(self, inputpath, outputpath):
        self.logger.info("--------------------------------------------------------------------------------")
        self.logger.info(f"extract agt columns from {inputpath} and save to {outputpath}")
        self.logger.info("--------------------------------------------------------------------------------")

        df = pd.read_csv(inputpath)
        cols = df.columns.values.tolist()[:2] # get the timestamp and firmware version columns
        cols.extend(AGT_COLS) # combine timestamp and firmware version columns with AGT_COLS. list.extend() operates in-place.
        df = self.__filter_csv_cols(df, cols)
        df.to_csv(outputpath, index=False)
        self.logger.info(f"saved to {outputpath}")


    

