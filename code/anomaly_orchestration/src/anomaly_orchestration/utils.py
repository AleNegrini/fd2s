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
