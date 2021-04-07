import unittest
import pandas as pd
import numpy as np
from pandas._testing import assert_frame_equal
from src.wtemp_failure_detection.signal_helper import time_series_helper

class TestSignalHelper(unittest.TestCase):


    def test_signal_frequency_equalizer_case1(self):
        ts = time_series_helper()

        sample_signal = pd.DataFrame({'test': [1, 1, 1, 1, 1, 1, 1, 1]})
        on_wrist_test = pd.DataFrame({'on_wrist': [1, 1]})

        actual_output = ts.signal_frequency_equalizer(4,
                                                      'on_wrist',
                                                      on_wrist_test,
                                                      sample_signal)

        expected_output = pd.DataFrame({'on_wrist': [1, 1, 1, 1, 1, 1, 1, 1]})

        assert_frame_equal(actual_output, expected_output)


    def test_signal_frequency_equalizer_case2(self):
        ts = time_series_helper()

        sample_signal = pd.DataFrame({'test': [1, 1, 1, 1, 1, 1, 1, 1]})
        on_wrist_test = pd.DataFrame({'on_wrist': [0, 0]})

        actual_output = ts.signal_frequency_equalizer(4,
                                                      'on_wrist',
                                                      on_wrist_test,
                                                      sample_signal)

        expected_output = pd.DataFrame({'on_wrist': [0, 0, 0, 0, 0, 0, 0, 0]})

        assert_frame_equal(actual_output, expected_output)


    def test_signal_frequency_equalizer_case3(self):
        ts = time_series_helper()

        sample_signal = pd.DataFrame({'test': [1, 1, 1, 1, 1, 1, 1, 1]})
        on_wrist_test = pd.DataFrame({'on_wrist': [1, 0]})

        actual_output = ts.signal_frequency_equalizer(4,
                                                      'on_wrist',
                                                      on_wrist_test,
                                                      sample_signal)

        expected_output = pd.DataFrame({'on_wrist': [1, 1, 1, 1, 0, 0, 0, 0]})

        assert_frame_equal(actual_output, expected_output)


    def test_concat_two_time_series(self):
        ts = time_series_helper()

        data = np.array([1, 1, 1, 1, 1, 1, 1, 1])
        df1 = pd.Series(data)
        df2 = pd.Series(data)

        actual_output = ts.concat_two_time_series(df1, df2, 'col1', 'col2')
        expected_output = pd.DataFrame({'col1': [1, 1, 1, 1, 1, 1, 1, 1],
                                       'col2': [1, 1, 1, 1, 1, 1, 1, 1]})

        assert_frame_equal(actual_output, expected_output)


    def test_get_temperature_on_wrist_only(self):
        ts = time_series_helper()

        input = pd.DataFrame({'w_temp': [1, 1, 1, 1, 1, 1, 1, 1],
                              'on_wrist': [1, 0, 0, 0, 0, 0, 0, 1]})

        actual_output = ts.get_temperature_on_wrist_only(input, 'res')

        expected_output = pd.DataFrame({'w_temp': [1, 1],
                                        'on_wrist': [1, 1],
                                        'res': [1, 1]})

        actual_output = actual_output.reset_index(drop=True)

        assert_frame_equal(actual_output, expected_output)


    def test_eval_roll_stats_metrics(self):
        ts = time_series_helper()

        input = pd.DataFrame({'index': [0, 1, 2, 90, 4],
                              'temp': [0, 1, 2, 3, 4],
                                'wrist_temperature': [0, 1, 2, 90, 4]})
        window = 2

        actual_output = ts.eval_roll_stats_metrics(window, input)

        expected_output = pd.DataFrame({'index': [0, 1, 2, 90, 4],
                                        'temp': [0, 1, 2, 3, 4],
                                        'wrist_temperature': [0, 1, 2, 90, 4],
                                        'roll_avg': [None, 0.5, 1.5, 46, 47],
                                        'roll_std': [None, 0.707107, 0.707107, 62.225397, 60.811183],
                                        'upper_band': [None, 2.62132, 3.62132, 232.67619, 229.43355],
                                        'lower_band': [None, -1.62132, -0.62132, -140.67619, -135.43355]})

        assert_frame_equal(actual_output[['index','temp','wrist_temperature','roll_avg','roll_std','upper_band','lower_band']], expected_output)