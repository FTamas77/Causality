import json
import os
import shutil
from pathlib import Path


class configurator:
    __instance = None

    __ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
    __CONFIG_FILE = os.path.join(__ROOT_DIR, 'causality',
                                 'measurement_config.json')
    __DEFAULT_CONFIG_FILE = os.path.join(__ROOT_DIR, 'causality',
                                         'measurement_config_default.json')
    __INPUT_DATA_DIR = os.path.join(__ROOT_DIR, 'dataset')

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        if not configurator.__instance:
            configurator.__instance = configurator.__configurator()
            self.__reread()

    def __get_config(self):
        with open(self.__CONFIG_FILE, encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data

    def __reread(self):
        data = self.__get_config()

        self.applied_input_files = []
        self.applied_input_files = data['input_files']

        causal_discovery_keep_cols = []
        self.causal_discovery_keep_cols = data['causal_discovery_keep_cols']

        self.causal_discovery_keep_cols_label = []
        self.causal_discovery_keep_cols_label = data[
            'causal_discovery_keep_cols_label']

        self.causal_inference_keep_cols = []
        self.causal_inference_keep_cols = data['causal_inference_keep_cols']

    def get_causal_discovery_keep_cols(self):
        return self.__instance.causal_discovery_keep_cols

    def get_causal_discovery_keep_cols_labels(self):
        return self.__instance.causal_discovery_keep_cols_label

    def get_causal_inference_keep_cols(self):
        return self.__instance.causal_inference_keep_cols

    def get_applied_input_files(self):
        return self.__instance.applied_input_files

    def get_CONFIG_FILE(self):
        return self.__instance.__CONFIG_FILE

    def get_ROOT_DIR(self):
        return self.__instance.__ROOT_DIR

    def get_INPUT_DATA_DIR(self):
        return self.__instance.__INPUT_DATA_DIR

    def get_config(self):
        return self.__instance.__get_config()

    def write_and_reset(self, data):
        file = open(self.__instance.__CONFIG_FILE, "w", encoding='utf-8')
        file.write(data)
        file.close()

        self.__reread()

    def default(self):
        os.remove(self.__instance.__CONFIG_FILE)
        shutil.copyfile(self.__instance.__DEFAULT_CONFIG_FILE,
                        self.__instance.__CONFIG_FILE)

        self.__reread()
