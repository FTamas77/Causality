from tkinter.simpledialog import askinteger
from tkinter import messagebox
from tkinter import *
import tkinter as tk
from tkinter import ttk

from data_reader import data_reader
from causal_inference import Causal_inference
from causal_discovery import Causal_discovery

import dowhy.plotter
import dowhy

import logging
import json
import os
import io
from contextlib import redirect_stdout
from pathlib import Path

ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
CONFIG_FILE = os.path.join(ROOT_DIR, 'causality', 'measurement_config.json')

top = Tk()


def get_config(configuration_file):
    """_summary_

    Args:
        applied_input_files (array): list of input files
    """

    data = read_configuration(configuration_file)
    return data


def causal_inference(applied_input_files, progressBar, write_log):
    """_summary_

    Args:
        applied_input_files (array): list of input files
    """
    write_log.set_log("Causal_inference is called")

    keep_cols = ["teljesítmény", "CO2 kibocsátás gkm V7",
                 "hengerűrtartalom", "Elhaladási zaj dBA"]

    reader = data_reader(applied_input_files)
    df = reader.read_input_data(keep_cols)

    causality = Causal_inference()
    progressBar.config(value=10)

    write_log.set_log("Reading input data")
    # df = causality.read_input_data()
    progressBar.config(value=20)

    write_log.set_log("Create the model")
    model = causality.create_model(df)
    progressBar.config(value=30)

    write_log.set_log("Identify effect")
    estimand = causality.identify_effect(model)
    progressBar.config(value=40)

    write_log.set_log("Estimate effect")
    estimate = causality.estimate_effect(model, estimand)
    progressBar.config(value=80)
    # dowhy.plotter.plot_causal_effect(
    # estimate, df["teljesítmény"], df["CO2 kibocsátás gkm V7"])

    write_log.set_log("Refute")
    causality.refute(model, estimand, estimate)
    progressBar.config(value=100)


def causal_discovery(applied_input_files, progressBar, write_log):
    """_summary_

    Args:
        applied_input_files (array): list of input files
    """

    write_log.set_log("Discovery is called")

    # simple or extended
    keep_cols = ["teljesítmény", "CO2 kibocsátás gkm V7",
                 "hengerűrtartalom", "Elhaladási zaj dBA",
                 "Összevont átlagfogy", "Korr abszorp együttható", "kilométeróra állás", "gy fogy ért orszúton"]

    keep_cols_label = ["Performance", "CO2 emission",
                       "Cylinder cap.", "Passing noise",
                       "Sum. consumption", "Corr. abs. co.", "Actual kilometers", "Cons. on roads"]

    reader = data_reader(applied_input_files)
    df = reader.read_input_data(keep_cols)

    causality = Causal_discovery()
    progressBar.config(value=20)

    write_log.set_log("read input data")
    # df = causality.read_input_data()
    progressBar.config(value=40)

    write_log.set_log("pc")
    causality.calculate_pc(df)
    progressBar.config(value=60)

    write_log.set_log("fci")
    causality.calculate_fci(df)
    progressBar.config(value=80)

    write_log.set_log("ges")
    causality.calculate_ges(df)
    progressBar.config(value=100)


def read_configuration(CONFIG_FILE):
    with open(CONFIG_FILE) as json_file:
        data = json.load(json_file)
    return data


class Output:
    def __init__(self, text_widget):
        self.text_space = text_widget

    def set_log(self, inputStr):
        self.text_space.insert('1.0', inputStr)
        self.text_space.insert('1.0', "\n")
        top.update()

def main():
    print("Starting.")
    print("Reading configuration.")
    data = get_config(CONFIG_FILE)

    applied_input_files = []
    # applied_input_file = data['input_files']
    applied_input_files = data['input_file_test']

    top.title("Causality")
    content = ttk.Frame(top, padding=(3, 3, 3, 3))
    content.grid(column=0, row=0)

    title = ttk.Label(
        content, text="Causal inference and discovery computation:")
    progressBar = ttk.Progressbar(
        content, length=400, orient=HORIZONTAL, mode='determinate', maximum=100, value=0)
    outputtext = tk.Text(content, wrap='word', height=11, width=50)
    write_log = Output(outputtext)
    causal_inference_button = ttk.Button(content, text="causal inference",
                                         command=lambda: causal_inference(applied_input_files, progressBar, write_log))
    causal_discovery_button = ttk.Button(content, text="causal discovery",
                                         command=lambda: causal_discovery(applied_input_files, progressBar, write_log))
    exit_button = ttk.Button(content, text="exit", command=top.destroy)

    title.grid(column=0, row=1)
    causal_inference_button.grid(column=0, row=2, sticky=(N, W), pady=5)
    causal_discovery_button.grid(column=0, row=3, sticky=(N, W), pady=5)
    exit_button.grid(column=0, row=4, sticky=(N, W), pady=5)
    progressBar.grid(column=1, row=4, sticky=(N, W), pady=5)
    outputtext.grid(column=0, row=5, columnspan=2,
                    sticky='NSWE', padx=5, pady=5)

    top.mainloop()

if __name__ == "__main__":
    main()

