import numpy as np
from pandas import DataFrame, Series
import pandas as pd

class time_series_helper:
    """
    Helper class that exposes a few useful methods for dealing with pandas timeseries
    """

    def signal_frequency_equalizer(self,
                                   target_frequency: int,
                                   column: str,
                                   df: DataFrame) -> DataFrame:
        """
        Create a signal with a target signal
        :param target_frequency: target frequency
        :param column: reference column
        :param df: Dataframe to process
        :return: dataframe with the new frequency
        """
        arr = pd.DataFrame(0, index=np.arange(len(df) * target_frequency), columns=[column])
        for index, value in arr[column].items():
            arr[column][index] = df[column][int(index / target_frequency)]

        return arr

    def sample_signal(self,
                      column: str,
                      df: DataFrame) -> DataFrame:
        """
        Sampling input signal
        :param column: reference column
        :param df: dataframe to sample
        :return: dataframe sampled
        """
        arr = pd.DataFrame(0, index=np.arange(int(len(df) / 16)), columns=[column])
        for index in range(0, int(len(df)), 16):
            arr[column][index / 16] = df[column][int(index)]

        return arr

    def concat_two_series(self,
                          series1: Series,
                          series2: Series,
                          column1_name: str,
                          column2_name: str) -> DataFrame:
        """
        Union of two pandas series
        :param series1: first series
        :param series2: second series
        :param column1_name: first series column
        :param column2_name: second series column
        :return:
        """
        data = {column1_name: series1,
                column2_name: series2}
        return pd.concat(data, axis=1)

    def get_ppg_on_wrist_only(self,
                              df: DataFrame,
                              column_name: str):
        """
        Method that returns a DataFrame with an additional column, containing the samples of PPG values
        when the device is worn
        :param df: dataframe to eval
        :param column_name: new column name
        :return: new dataframe
        """
        df[column_name] = df.apply(lambda row: row.ppg * row.on_wrist, axis=1)
        df = df.drop(df[df[column_name] == 0].index)
        return df