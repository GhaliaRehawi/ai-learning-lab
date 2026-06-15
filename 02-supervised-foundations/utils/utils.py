import sys
import yaml
import logging


def read_config_file(path: str) -> dict:
    """
    Reads a .yaml config file into a dict.

    Args:
        path: str
            Path to the config file.

    Returns:
        config: dict
            Parameters specified in the config file.
    """
    with open(path, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError:
            print('Could not load config file!')

    return config