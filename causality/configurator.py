import json
import os
from pathlib import Path


class configurator:

    ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
    CONFIG_FILE = os.path.join(ROOT_DIR, 'causality',
                               'measurement_config.json')
    INPUT_DATA_DIR = os.path.join(ROOT_DIR, 'dataset')

    class __configurator:

        # Receive the json file and process here
        def __init__(self, applied_input_files):
            # simple or extended
            # simple is the first four cols
            # TODO: store these in the JSON config file.
            self.causal_discovery_keep_cols = [
                "teljesítmény", "CO2 kibocsátás gkm V7", "hengerűrtartalom",
                "Elhaladási zaj dBA", "Összevont átlagfogy",
                "Korr abszorp együttható", "kilométeróra állás",
                "gy fogy ért orszúton"
            ]
            self.causal_discovery_keep_cols_label = [
                "Performance", "CO2 emission", "Cylinder cap.",
                "Passing noise", "Sum. consumption", "Corr. abs. co.",
                "Actual kilometers", "Cons. on roads"
            ]
            self.causal_inference_keep_cols = [
                "teljesítmény",
                "CO2 kibocsátás gkm V7",
                "hengerűrtartalom",
                "Elhaladási zaj dBA",
            ]

            self.applied_input_files = applied_input_files

    instance = None

    def __get_config(self):
        with open(configurator.CONFIG_FILE) as json_file:
            data = json.load(json_file)
        return data

    def __init__(self):
        if not configurator.instance:
            # In case of further options, read all of them here,
            # then pass to the instance
            data = self.__get_config()

            applied_input_files = []
            applied_input_files = data[
                'input_file_test']  # data['input_files']

            configurator.instance = configurator.__configurator(
                applied_input_files)

    def get_causal_discovery_keep_cols(self):
        return configurator.instance.causal_discovery_keep_cols

    def get_causal_discovery_keep_cols_labels(self):
        return configurator.instance.causal_discovery_keep_cols_label

    def get_causal_inference_keep_cols(self):
        return configurator.instance.causal_inference_keep_cols

    def get_applied_input_files(self):
        return configurator.instance.applied_input_files

    def get_CONFIG_FILE(self):
        return configurator.CONFIG_FILE

    def get_ROOT_DIR(self):
        return configurator.ROOT_DIR

    def get_INPUT_DATA_DIR(self):
        return configurator.INPUT_DATA_DIR
