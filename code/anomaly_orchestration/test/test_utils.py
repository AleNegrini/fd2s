import unittest
import os
from src.anomaly_orchestration.utils import Utils

class TestUtils(unittest.TestCase):

    def test_get_environment_missing_key(self):
        self.assertEqual(Utils.get_environment(key_name='MISSINGKEY',
                                 default='Foo'),'Foo')

    def test_get_environment_key(self):
        os.environ['ENV'] = 'PRODUCTION'
        self.assertEqual(Utils.get_environment(key_name='ENV',
                                               default='Foo'), 'PRODUCTION')