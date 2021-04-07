import os
from typing import Any

class Utils:

    @staticmethod
    def get_environment(key_name: str, default: Any) -> Any:
        """
        Get the environment variable value
        :param key_name: environment variable key
        :param default: default value
        :return: the value of the environment variable
        """

        try:
            return os.environ[key_name]
        except KeyError:
            return default

    @staticmethod
    def build_item_dynamoDB(device_id: str,
                            date: str,
                            min: str,
                            avg: str,
                            max: str,
                            timestamp: str,
                            avg_anomaly: str,
                            max_anomaly: str,
                            min_anomaly: str):

        return {
            'DeviceId': {'S': device_id},
            'Date': {'S': date},
            'min': {'S': min},
            'min_anomaly': {'S': min_anomaly},
            'avg': {'S': avg},
            'avg_anomaly': {'S': avg_anomaly},
            'max': {'S': max},
            'max_anomaly': {'S': max_anomaly},
            'timestamp': {'S': timestamp},
        }
