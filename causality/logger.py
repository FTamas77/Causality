from tkinter.simpledialog import askinteger
from tkinter import messagebox
from tkinter import *
import tkinter as tk
from tkinter import ttk


class logger:
    class __logger:
        def __init__(self, top, text_widget):
            self.top = top
            self.text_widget = text_widget

        def __str__(self):
            return repr(self) + self.top + self.text_widget

    instance = None

    def __init__(self, top, text_widget):
        if not logger.instance:
            logger.instance = logger.__logger(top, text_widget)
        else:
            logger.instance.top = top
            logger.instance.text_widget = text_widget

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def print_log(self, inputStr):
        self.instance.text_widget.insert('1.0', inputStr)
        self.instance.text_widget.insert('1.0', "\n")
        self.instance.top.update()
