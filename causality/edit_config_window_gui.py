from tkinter import *
from tkinter import scrolledtext

from configurator import configurator


class edit_config_window_gui(Toplevel):

    def __init__(self, top):
        super().__init__(master=top)
        self.c = configurator()
        self.initUI()

    def initUI(self):
        self.title("Edit configuration")
        self.geometry("200x200")

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        lbl = Label(self, text="JSON configuration:")
        lbl.grid(sticky=W, pady=4, padx=5)

        self.textPad = scrolledtext.ScrolledText(self)
        self.textPad.grid(row=1,
                          column=0,
                          columnspan=2,
                          rowspan=4,
                          padx=5,
                          sticky=E + W + S + N)

        abtn = Button(self, text="Save", command=self.save_command)
        abtn.grid(row=1, column=3)

        cbtn = Button(self, text="Close", command=self.onExit)
        cbtn.grid(row=2, column=3, pady=4)

        # the configuration file is fixed
        file = self.c.get_CONFIG_FILE()
        with open(file, encoding='utf-8') as f:
            contents = f.readlines()
            self.textPad.insert('1.0', contents)
            file.close()

    def onExit(self):
        self.destroy()

    def save_command(self):
        f = open(self.c.get_CONFIG_FILE(), "w")
        # slice off the last character from get, as an extra return is added
        data = self.textPad.get('1.0', 'end-1c')
        f.write(data)
        f.close()
