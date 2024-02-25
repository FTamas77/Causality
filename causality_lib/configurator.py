import json
import os
import shutil
from pathlib import Path

from jsonschema import validate


class configurator:
    __instance = None

    __ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
    __CONFIG_FILE = os.path.join(__ROOT_DIR, "causality_lib", "measurement_config.json")
    __CONFIG_SCHEMA_FILE = os.path.join(
        __ROOT_DIR, "causality_lib", "measurement_config_schema.json"
    )
    __DEFAULT_CONFIG_FILE = os.path.join(
        __ROOT_DIR, "causality_lib", "measurement_config_default.json"
    )
    __INPUT_DATA_DIR = os.path.join(__ROOT_DIR, "dataset")

    __CAUSAL_GRAPH_CONFIG_FILE = os.path.join(
        __ROOT_DIR, "causality_lib", "measurement_causal_graph"
    )
    __DEFAULT_CAUSAL_GRAPH_CONFIG_FILE = os.path.join(
        __ROOT_DIR, "causality_lib", "measurement_causal_graph_default"
    )

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        cls.__instance.__reread()
        return cls.__instance

    def __init__(self):
        if not configurator.__instance:
            configurator.__instance = configurator.__configurator()
            self.__reread()

    def __get_config(self):
        with open(self.__CONFIG_FILE, encoding="utf-8") as json_file:
            data = json.load(json_file)

        with open(self.__CONFIG_SCHEMA_FILE, encoding="utf-8") as json_file:
            schema = json.load(json_file)

        try:
            validate(data, schema)
        except jsonschema.ValidationError as e:
            print(e.message)
        except jsonschema.SchemaError as e:
            print(e)

        return data

    def __get_causal_graph(self):
        with open(self.__CAUSAL_GRAPH_CONFIG_FILE, encoding="utf-8") as file:
            causal_graph = file.read()

        return causal_graph

    def __reread(self):
        data = self.__get_config()
        causal_graph = self.__get_causal_graph()

        self.applied_input_files = []
        self.applied_input_files = data["input_files"]

        causal_discovery_keep_cols = []
        self.causal_discovery_keep_cols = data["causal_discovery_keep_cols"]

        self.causal_discovery_keep_cols_label = []
        self.causal_discovery_keep_cols_label = data["causal_discovery_keep_cols_label"]

        self.causal_inference_keep_cols = []
        self.causal_inference_keep_cols = data["causal_inference_keep_cols"]

        self.__causal_inference_treatment = data["treatment"]
        self.__causal_inference_outcome = data["outcome"]

        self.__causal_inference_causal_graph = causal_graph

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

    def get_treatment(self):
        return self.__instance.__causal_inference_treatment

    def get_outcome(self):
        return self.__instance.__causal_inference_outcome

    def get_causal_graph(self):
        return self.__instance.__causal_inference_causal_graph

    def write_and_reset(self, data):
        file = open(self.__instance.__CONFIG_FILE, "w", encoding="utf-8")
        file.write(data)
        file.close()

        self.__reread()

    def write_and_reset_causal_graph(self, data):
        file = open(self.__instance.__CAUSAL_GRAPH_CONFIG_FILE, "w", encoding="utf-8")
        file.write(data)
        file.close()

        self.__reread()

    def default(self):
        os.remove(self.__instance.__CONFIG_FILE)
        shutil.copyfile(
            self.__instance.__DEFAULT_CONFIG_FILE, self.__instance.__CONFIG_FILE
        )

        self.__reread()

    def default_causal_graph(self):
        os.remove(self.__instance.__CAUSAL_GRAPH_CONFIG_FILE)
        shutil.copyfile(
            self.__instance.__DEFAULT_CAUSAL_GRAPH_CONFIG_FILE,
            self.__instance.__CAUSAL_GRAPH_CONFIG_FILE,
        )

        self.__reread()
