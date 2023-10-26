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

    def __put_to_grid(self):
        self.title.grid(
            column=0,
            row=1,
            columnspan=2,
        )
        self.causal_inference_button.grid(column=0,
                                          row=2,
                                          sticky=(N, W),
                                          pady=5)

        self.causal_discovery_button.grid(column=0,
                                          row=3,
                                          sticky=(N, W),
                                          pady=5)

        self.exit_button.grid(column=0, row=4, sticky=(N, W), pady=5)
        self.progressBar.grid(column=1, row=4, sticky=(N, W), pady=5)
        self.outputtext.grid(column=0,
                             row=5,
                             columnspan=2,
                             sticky='NSWE',
                             padx=5,
                             pady=5)

    def __format_gui(self):
        Font_tuple = ("Comic Sans MS", 15, "bold")
        self.title.configure(font=Font_tuple)

    def build_gui(self):
        self.top.title("Causality")
        self.content = ttk.Frame(self.top, padding=(3, 3, 3, 3))
        self.content.grid(column=0, row=0)
        self.title = ttk.Label(
            self.content, text="Causal inference and discovery computation:")

        self.progressBar = ttk.Progressbar(self.content,
                                           length=300,
                                           orient=HORIZONTAL,
                                           mode='determinate',
                                           maximum=100,
                                           value=0)

        self.outputtext = tk.Text(self.content,
                                  wrap='word',
                                  height=11,
                                  width=50)

        # TODO: we create it here, because it need variables, but it is a singleton
        self.logger_obj = logger(self.top, self.outputtext)

        style = ttk.Style()
        style.theme_use('alt')
        style.configure('TButton',
                        background='green',
                        foreground='white',
                        width=15,
                        borderwidth=1,
                        focusthickness=3,
                        focuscolor='none')
        style.map('TButton', background=[('active', 'green')])
        self.causal_inference_button = ttk.Button(
            self.content,
            text="Causal inference",
            command=lambda: causal_algs.causal_inference(self.progressBar))

        self.causal_discovery_button = ttk.Button(
            self.content,
            text="Causal discovery",
            command=lambda: causal_algs.causal_discovery(self.progressBar))

        self.exit_button = ttk.Button(self.content,
                                      text="exit",
                                      command=self.top.destroy)

        self.__format_gui()
        self.__put_to_grid()

    def start_gui(self):
        self.top.mainloop()
