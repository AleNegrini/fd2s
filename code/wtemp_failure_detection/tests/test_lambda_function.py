import unittest
from src.ppg_failure_detection.lambda_function import read_csv_df

class TestPandasReadDF(unittest.TestCase):

    def test_read_csv_df(self):
        test_df = read_csv_df(path='./test_resource/test.csv',
                              columns=['test_col'])
        self.assertEqual(len(test_df), 4)
        self.assertEqual(test_df['test_col'][0], 30)

if __name__ == '__main__':
    unittest.main()