from tkinter import *
from tkinter import ttk


class GUI:

    def __init__(self):
        self.root = Tk()
        self.root.title("Youtube Backup V0.0")
        self.mainframe = ttk.Frame()
        self.mainframe.grid()
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def home(self):
        pass
