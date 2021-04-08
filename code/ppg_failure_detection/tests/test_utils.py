import unittest
import os
from src.ppg_failure_detection.ppg_utils import Utils

class TestUtils(unittest.TestCase):

    def test_get_environment_missing_key(self):
        self.assertEqual(Utils.get_environment(key_name='MISSINGKEY',
                                               default='Foo'), 'Foo')

    def test_get_environment_key(self):
        os.environ['ENV'] = 'PRODUCTION'
        self.assertEqual(Utils.get_environment(key_name='ENV',
                                               default='Foo'), 'PRODUCTION')

    def test_build_item_dynamoDB(self):
        actual_obj = Utils.build_item_dynamoDB(device_id='device_001',
                                        date='2020/01/01',
                                        min='200',
                                        avg='10',
                                        max='10',
                                        timestamp='2020/02/02T00:00:00',
                                        avg_anomaly='YES',
                                        max_anomaly='NO',
                                        min_anomaly='YES')

        expected_object = {
            'DeviceId': {'S': 'device_001'},
            'Date': {'S': '2020/01/01'},
            'min': {'S': '200'},
            'min_anomaly': {'S': 'YES'},
            'avg': {'S': '10'},
            'avg_anomaly': {'S': 'YES'},
            'max': {'S': '10'},
            'max_anomaly': {'S': 'NO'},
            'timestamp': {'S': '2020/02/02T00:00:00'}
        }

        self.assertDictEqual(actual_obj, expected_object)
