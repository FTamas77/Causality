from tkinter import *
import tkinter as tk
from tkinter import ttk

from logger import logger
from causal_algs import causal_algs




class gui:

    def __init__(self):
        self.top = Tk()
        self.title = None
        self.outputtext = None
        self.causal_inference_button = None
        self.causal_discovery_button = None
        self.exit_button = None
        self.content = None

    def build_gui(self, applied_input_files):
        self.top.title("Causality")
        self.content = ttk.Frame(self.top, padding=(3, 3, 3, 3))
        self.content.grid(column=0, row=0)

        self.title = ttk.Label(
            self.content, text="Causal inference and discovery computation:")
        self.progressBar = ttk.Progressbar(
            self.content, length=400, orient=HORIZONTAL, mode='determinate', maximum=100, value=0)

        # TODO: gui has a logger
        self.outputtext = tk.Text(
            self.content, wrap='word', height=11, width=50)
        self.logger_obj = logger(self.top, self.outputtext)

        self.causal_inference_button = ttk.Button(self.content, text="causal inference",
                                                  command=lambda: causal_algs.causal_inference(applied_input_files, self.progressBar, self.logger_obj))
        self.causal_discovery_button = ttk.Button(self.content, text="causal discovery",
                                                  command=lambda: causal_algs.causal_discovery(applied_input_files, self.progressBar, self.logger_obj))
        self.exit_button = ttk.Button(
            self.content, text="exit", command=self.top.destroy)

        # put objects on the grid
        self.title.grid(column=0, row=1)
        self.causal_inference_button.grid(
            column=0, row=2, sticky=(N, W), pady=5)
        self.causal_discovery_button.grid(
            column=0, row=3, sticky=(N, W), pady=5)
        self.exit_button.grid(column=0, row=4, sticky=(N, W), pady=5)
        self.progressBar.grid(column=1, row=4, sticky=(N, W), pady=5)
        self.outputtext.grid(column=0, row=5, columnspan=2,
                             sticky='NSWE', padx=5, pady=5)

    def start_gui(self):
        self.top.mainloop()
