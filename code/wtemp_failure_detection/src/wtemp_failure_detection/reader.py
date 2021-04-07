import numpy as np
from pandas import DataFrame
import pandas as pd

class Reader:

    @staticmethod
    def read_csv_df(path: str,
                    columns:list) -> DataFrame:
        """
        It reads the csv in a Dataframe pandas
        :param path: path where the file is
        :param columns: columns name
        :return: pandas dataframe containing the csv
        """
        dtype = {}
        for col in columns:
            dtype[col] = np.int32
        return pd.read_csv(filepath_or_buffer=path,
                           names=columns,
                           dtype=dtype)