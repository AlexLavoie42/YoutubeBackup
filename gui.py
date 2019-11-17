import abc
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from manager import VideoManager
from util import threaded


class GUI(abc.ABC):

    def __init__(self, title, manager=VideoManager()):
        self.manager = manager
        self.root = Tk()
        self.root.title(title)
        self.mainframe = ttk.Frame()
        self.mainframe.grid()
        self.mainframe.grid(column=20, row=20, sticky=(N, W, E, S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    @abc.abstractmethod
    def run(self):
        pass


class HomeGUI(GUI):

    def __init__(self, title):
        super().__init__(title)
        self.folder = ""

    def run(self):
        def __login(s):
            s.manager.login()
            login_button['state'] = DISABLED
            download_button['state'] = 'normal'
            upload_button['state'] = 'normal'

        url = ""
        url_label = ttk.Label(self.mainframe,
                              text="Enter Video URL To Download")
        url_input = ttk.Entry(self.mainframe, width=30, textvariable=url)
        download_button = ttk.Button(self.mainframe,
                                     text="Download",
                                     command=lambda:
                                     threaded(lambda:
                                              self.manager.save_videos(
                                                  url_input.get())))
        login_button = ttk.Button(self.mainframe,
                                  text="Login",
                                  command=lambda: threaded(lambda:
                                                           __login(self)))
        browse_button = ttk.Button(self.mainframe,
                                   text="Browse",
                                   command=self.set_path)
        upload_button = ttk.Button(self.mainframe,
                                   text="Upload",
                                   command=lambda:
                                   self.threaded_with_path(
                                       self.manager.post_video))

        login_button.grid(column=0, row=0, sticky=W, pady=10, padx=10)
        url_label.grid(column=0, row=1, padx=10)
        url_input.grid(column=1, row=1, padx=10)
        download_button.grid(column=1, row=3)
        browse_button.grid(column=0, row=4, pady=10)
        upload_button.grid(column=2, row=4, pady=10, padx=10)

        download_button['state'] = DISABLED
        upload_button['state'] = DISABLED

        self.root.mainloop()

    def threaded_with_path(self, func):
        if self.folder != "":
            threaded(lambda: func(self.folder))

    def set_path(self):
        self.folder = filedialog.askdirectory()
        self.manager.change_folder(self.folder)
        current_video = ttk.Label(self.mainframe,
                                  text=f"{self.folder}")
        current_video.grid(column=1, row=4, pady=10)


if __name__ == '__main__':
    gui = HomeGUI("Youtube Backup V1.1")
    gui.run()
