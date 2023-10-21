from causal_inference import Causal_inference
from causal_discovery import Causal_discovery

import dowhy.plotter
import dowhy

import logging
import json
import os
from pathlib import Path

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
CONFIG_FILE = os.path.join(ROOT_DIR, 'causality', 'measurement_config.json')


def causal_inference(applied_input_file):
    causality = Causal_inference(applied_input_file)

    df = causality.read_input_data()
    model = causality.create_model(df)
    estimand = causality.identify_effect(model)

    estimate = causality.estimate_effect(model, estimand)
    # dowhy.plotter.plot_causal_effect(
    # estimate, df["teljesítmény"], df["CO2 kibocsátás gkm V7"])

    causality.refute(model, estimand, estimate)


def causal_discovery(applied_input_file):
    causality = Causal_discovery(applied_input_file)

    df = causality.read_input_data()
    causality.calculate_pc(df)
    causality.calculate_fci(df)
    causality.calculate_ges(df)


def main(applied_input_file):
    causal_inference(applied_input_file)
    causal_discovery(applied_input_file)


def read_configuration(CONFIG_FILE):
    with open(CONFIG_FILE) as json_file:
        data = json.load(json_file)

    return data


if __name__ == "__main__":
    data = read_configuration(CONFIG_FILE)

    print("Read the following input files:\n")
    for input_file in data['input_files']:
        print(input_file)

    applied_input_file = data['input_files']

    # applied_input_file = data['input_file_test']
    main(applied_input_file)
