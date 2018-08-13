import tkinter
import os
import pickle
import webbrowser
from interface import open_popup


class Menu(object):

    def __init__(self, root, main_window, logger):
        self.root = root
        self.menu = tkinter.Menu(self.root)
        self.root.config(menu=self.menu)
        self.add()
        self.main_window = main_window
        self.log = logger

    def add(self):
        file_menu = tkinter.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_command(label="Open...", command=self.open)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

        help_menu = tkinter.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About...", command=self.open_readme)

    def save(self):
        data = self.main_window.canvas.get_all_project_properties()
        save_location = str(data['project_directory'])
        file_name = str(data['canvas_name'])
        full_path = save_location + '/' + file_name + '.pkl'
        with open(os.path.expanduser(full_path), 'wb') as file:
            pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)

    def open(self):
        open_popup.OpenPopup(self.main_window, self.log)

    @staticmethod
    def open_readme():
        webbrowser.open_new('https://github.com/mcgridles/neuromatic/blob/master/README.md')
