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
                                   original_df: DataFrame,
                                   reference_df: DataFrame) -> DataFrame:
        """
        Create a signal with a target signal
        :param target_frequency: target frequency
        :param column: reference column
        :param original_df: original Dataframe
        :param reference_df: target Dataframe frequency
        :return: dataframe with the new frequency
        """
        arr = pd.DataFrame(0, index=np.arange(len(reference_df)), columns=[column])
        for index, value in arr[column].items():
            arr[column][index] = original_df[column][int(index / target_frequency)]
        return arr

    def concat_two_time_series(self,
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

    def get_temperature_on_wrist_only(self,
                                      df: DataFrame,
                                      column_name: str):
        """
        Method that returns a DataFrame with an additional column, containing the samples of temperature
        when the device is worn
        :param df: dataframe to eval
        :param column_name: new column name
        :return: new dataframe
        """
        df[column_name] = df.apply(lambda row: row.on_wrist * row.w_temp, axis=1)
        df = df.drop(df[df[column_name] == 0].index)
        return df

    def eval_roll_stats_metrics(self,
                                window: int,
                                df: DataFrame) -> DataFrame:
        """
        Method that evaluates a set of statistical columns
        :param window: window
        :param df: dataframe to apply statistics on
        :return: dataframe with the new statistics
        """
        df.index = range(len(df))
        df['roll_avg'] = df.iloc[:, 2].rolling(window=window).mean()
        df['roll_std'] = df.iloc[:, 2].rolling(window=window).std()
        df['upper_band'] = df.apply(lambda row: row.roll_avg + 3 * row.roll_std, axis=1)
        df['lower_band'] = df.apply(lambda row: row.roll_avg - 3 * row.roll_std, axis=1)
        df['discostamento_pos'] = df.apply(
            lambda row: row.wrist_temperature - row.upper_band if row.wrist_temperature > row.upper_band else None, axis=1)
        df['discostamento_neg'] = df.apply(
            lambda row: row.lower_band - row.wrist_temperature if row.wrist_temperature < row.lower_band else None, axis=1)
        df['discostamento'] = df.discostamento_pos.combine_first(df.discostamento_neg)

        return df
