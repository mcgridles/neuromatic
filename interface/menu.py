import tkinter
import os
import pickle
from interface import open_popup


class Menu(object):

    def __init__(self, root, main_window, logger):
        self.menu = tkinter.Menu(root)
        root.config(menu=self.menu)
        self.add()
        self.main_window = main_window
        self.log = logger

    def add(self):
        file_menu = tkinter.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_command(label="Open...", command=self.open)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=callback)

        help_menu = tkinter.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About...", command=callback)

    def save(self):
        data = self.main_window.slots.get_all_project_properties()
        save_location = str(data['project_directory'])
        file_name = str(data['canvas_name'])
        full_path = save_location + '/' + file_name + '.txt'
        with open(os.path.expanduser(full_path), 'wb') as file:
            pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)

    def open(self):
        open_popup.OpenPopup(self.main_window, self.log)
