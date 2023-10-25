from tkinter.simpledialog import askinteger
from tkinter import messagebox
from tkinter import *
import tkinter as tk
from tkinter import ttk

from data_reader import data_reader
from logger import logger
from causal_algs import causal_algs
from gui import gui
from configurator import configurator

import dowhy.plotter
import dowhy

import logging
import json
import os
import io
from contextlib import redirect_stdout
from pathlib import Path


def main():
    # The configuration file is fix
    data = configurator.get_config()
    applied_input_files = []
    # applied_input_file = data['input_files']
    applied_input_files = data['input_file_test']

    g = gui()
    g.build_gui(applied_input_files)
    g.start_gui()


if __name__ == "__main__":
    main()
