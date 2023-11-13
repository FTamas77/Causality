from tkinter import *
from tkinter import scrolledtext
from tkinter import ttk

import json

from configurator import configurator


class edit_model_window_gui(Toplevel):

    def __init__(self, top):
        super().__init__(master=top)
        self.initUI()

    def __print_config_on_screen(self):
        c = configurator()
        data = c.get_causal_graph()
        self.textPad.delete('1.0', END)
        self.textPad.insert('1.0', data)

    def initUI(self):
        self.title("Edit causal graph")
        self.geometry("1200x600")

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        lbl = ttk.Label(self, text="Causal graph structure:")
        lbl.grid(sticky=W, pady=4, padx=5)

        self.textPad = scrolledtext.ScrolledText(self)
        self.textPad.grid(row=1,
                          column=0,
                          columnspan=2,
                          rowspan=4,
                          padx=5,
                          sticky=E + W + S + N)

        abtn = ttk.Button(self, text="Save", command=self.save_command)
        abtn.grid(row=1, column=3)

        cbtn = ttk.Button(self, text="Default", command=self.default)
        cbtn.grid(row=2, column=3, pady=4)

        cbtn = ttk.Button(self, text="Close", command=self.exit)
        cbtn.grid(row=4, column=3, pady=4)

        # the configuration file is fix
        self.__print_config_on_screen()

    def exit(self):
        self.destroy()

    def save_command(self):
        # slice off the last character from get, as an extra return is added
        data = self.textPad.get('1.0', 'end-1c')

        c = configurator()
        c.write_and_reset_causal_graph(data)

    def default(self):
        c = configurator()
        c.default_causal_graph()
        self.__print_config_on_screen()
