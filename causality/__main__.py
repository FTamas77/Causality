from tkinter.simpledialog import askinteger
from tkinter import messagebox
from tkinter import *
import tkinter as tk
from tkinter import ttk

from data_reader import data_reader
from logger import logger
from causal_algs import causal_algs

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


def read_configuration(CONFIG_FILE):
    with open(CONFIG_FILE) as json_file:
        data = json.load(json_file)
    return data


def get_config(configuration_file):
    data = read_configuration(configuration_file)
    return data


def build_gui(applied_input_files):
    top.title("Causality")
    content = ttk.Frame(top, padding=(3, 3, 3, 3))
    content.grid(column=0, row=0)

    title = ttk.Label(
        content, text="Causal inference and discovery computation:")
    progressBar = ttk.Progressbar(
        content, length=400, orient=HORIZONTAL, mode='determinate', maximum=100, value=0)
    outputtext = tk.Text(content, wrap='word', height=11, width=50)

    logger_obj = logger(top, outputtext)
    causal_inference_button = ttk.Button(content, text="causal inference",
                                         command=lambda: causal_algs.causal_inference(applied_input_files, progressBar, logger_obj))
    causal_discovery_button = ttk.Button(content, text="causal discovery",
                                         command=lambda: causal_algs.causal_discovery(applied_input_files, progressBar, logger_obj))
    exit_button = ttk.Button(content, text="exit", command=top.destroy)

    title.grid(column=0, row=1)
    causal_inference_button.grid(column=0, row=2, sticky=(N, W), pady=5)
    causal_discovery_button.grid(column=0, row=3, sticky=(N, W), pady=5)
    exit_button.grid(column=0, row=4, sticky=(N, W), pady=5)
    progressBar.grid(column=1, row=4, sticky=(N, W), pady=5)
    outputtext.grid(column=0, row=5, columnspan=2,
                    sticky='NSWE', padx=5, pady=5)


def main():

    data = get_config(CONFIG_FILE)
    applied_input_files = []
    # applied_input_file = data['input_files']
    applied_input_files = data['input_file_test']

    build_gui(applied_input_files)

    top.mainloop()


if __name__ == "__main__":
    main()
