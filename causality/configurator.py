import json
import os
from pathlib import Path

# TODO: add to member variables
ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
CONFIG_FILE = os.path.join(ROOT_DIR, 'causality', 'measurement_config.json')


class configurator:
    data = None

    @staticmethod
    def get_config():
        data = configurator.read_configuration(CONFIG_FILE)
        return configurator.data

    @staticmethod
    def read_configuration(CONFIG_FILE):
        with open(CONFIG_FILE) as json_file:
            configurator.data = json.load(json_file)
        return configurator.data
