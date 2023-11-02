import json
import os
from pathlib import Path


class configurator:

    __ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
    __CONFIG_FILE = os.path.join(__ROOT_DIR, 'causality',
                                 'measurement_config.json')
    __INPUT_DATA_DIR = os.path.join(__ROOT_DIR, 'dataset')

    class __configurator:

        def __init__(self, applied_input_files, causal_discovery_keep_cols,
                     causal_discovery_keep_cols_label,
                     causal_inference_keep_cols):
            self.applied_input_files = applied_input_files
            self.causal_discovery_keep_cols = causal_discovery_keep_cols
            self.causal_discovery_keep_cols_label = causal_discovery_keep_cols_label
            self.causal_inference_keep_cols = causal_inference_keep_cols

    instance = None

    def __get_config(self, configuration_file):
        with open(configuration_file, encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data

    def __init__(self, configuration_file=__CONFIG_FILE):
        if not configurator.instance:
            data = self.__get_config(configuration_file)

            applied_input_files = []
            applied_input_files = data['input_files']

            causal_discovery_keep_cols = []
            causal_discovery_keep_cols = data['causal_discovery_keep_cols']

            causal_discovery_keep_cols_label = []
            causal_discovery_keep_cols_label = data[
                'causal_discovery_keep_cols_label']

            causal_inference_keep_cols = []
            causal_inference_keep_cols = data['causal_inference_keep_cols']

            configurator.instance = configurator.__configurator(
                applied_input_files, causal_discovery_keep_cols,
                causal_discovery_keep_cols_label, causal_inference_keep_cols)

    def get_causal_discovery_keep_cols(self):
        return configurator.instance.causal_discovery_keep_cols

    def get_causal_discovery_keep_cols_labels(self):
        return configurator.instance.causal_discovery_keep_cols_label

    def get_causal_inference_keep_cols(self):
        return configurator.instance.causal_inference_keep_cols

    def get_applied_input_files(self):
        return configurator.instance.applied_input_files

    def get_CONFIG_FILE(self):
        return configurator.__CONFIG_FILE

    def get_ROOT_DIR(self):
        return configurator.__ROOT_DIR

    def get_INPUT_DATA_DIR(self):
        return configurator.__INPUT_DATA_DIR
