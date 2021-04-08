import unittest
import pandas as pd
import numpy as np
from pandas._testing import assert_frame_equal
from src.ppg_failure_detection.ts_signal_helper import time_series_helper

class TestSignalHelper(unittest.TestCase):


    def test_signal_frequency_equalizer_case1(self):
        ts = time_series_helper()

        sample_signal = pd.DataFrame({'test': [1, 1]})

        actual_output = ts.signal_frequency_equalizer(4,
                                                      'test',
                                                      sample_signal)

        expected_output = pd.DataFrame({'test': [1, 1, 1, 1, 1, 1, 1, 1]})

        assert_frame_equal(actual_output, expected_output)


    def test_signal_frequency_equalizer_case2(self):
        ts = time_series_helper()

        sample_signal = pd.DataFrame({'test': [0, 0]})

        actual_output = ts.signal_frequency_equalizer(4,
                                                      'test',
                                                      sample_signal)

        expected_output = pd.DataFrame({'test': [0, 0, 0, 0, 0, 0, 0, 0]})

        assert_frame_equal(actual_output, expected_output)


    def test_signal_frequency_equalizer_case3(self):
        ts = time_series_helper()

        on_wrist_test = pd.DataFrame({'on_wrist': [1, 0]})

        actual_output = ts.signal_frequency_equalizer(4,
                                                      'on_wrist',
                                                      on_wrist_test)

        expected_output = pd.DataFrame({'on_wrist': [1, 1, 1, 1, 0, 0, 0, 0]})

        assert_frame_equal(actual_output, expected_output)


    def test_concat_two_time_series(self):
        ts = time_series_helper()

        data = np.array([1, 1, 1, 1, 1, 1, 1, 1])
        df1 = pd.Series(data)
        df2 = pd.Series(data)

        actual_output = ts.concat_two_series(df1, df2, 'col1', 'col2')
        expected_output = pd.DataFrame({'col1': [1, 1, 1, 1, 1, 1, 1, 1],
                                       'col2': [1, 1, 1, 1, 1, 1, 1, 1]})

        assert_frame_equal(actual_output, expected_output)


    def test_get_temperature_on_wrist_only(self):
        ts = time_series_helper()

        input = pd.DataFrame({'ppg': [1, 1, 1, 1, 1, 1, 1, 1],
                              'on_wrist': [1, 0, 0, 0, 0, 0, 0, 1]})

        actual_output = ts.get_ppg_on_wrist_only(input, 'res')

        expected_output = pd.DataFrame({'ppg': [1, 1],
                                        'on_wrist': [1, 1],
                                        'res': [1, 1]})

        actual_output = actual_output.reset_index(drop=True)

        assert_frame_equal(actual_output, expected_output)

