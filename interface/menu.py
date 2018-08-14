import tkinter
import os
import pickle
import webbrowser
from interface import open_popup


class Menu(object):

    def __init__(self, root, main_window, logger):
        """
        The Menu exists at the top of the window and allows the user to save and load canvas designs, exit the
        application, and view the README.
        :param root: tkinter.Widget - The widget in which the menu will be encapsulated.
        :param main_window: tkinter.Tk - The main window on which the menu will exist.
        :param logger: function - The function to which status strings can be passed.
        """
        self.root = root
        self.menu = tkinter.Menu(self.root)
        self.root.config(menu=self.menu)
        self.add_buttons()
        self.main_window = main_window
        self.log = logger

    def add_buttons(self):
        """
        Add the buttons to the menu.
        :return: None
        """
        # Create the menu under "File"
        file_menu = tkinter.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_command(label="Open...", command=self.open)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

        # Create the menu under "Help"
        help_menu = tkinter.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About...", command=self.open_readme)

    def save(self):
        """
        Save the current canvas design to a file in the directory specified by the Canvas Properties Box.
        :return: None
        """
        # Get the canvas design from the main window.
        data = self.main_window.canvas.get_all_project_properties()
        save_location = str(data['project_directory'])
        file_name = str(data['canvas_name'])
        # Create the fill path to the file
        full_path = save_location + '/' + file_name + '.pkl'
        # Use pickle to serialize the information and save to the file
        with open(os.path.expanduser(full_path), 'wb') as file:
            pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)

    def open(self):
        """
        Open a widget that allows the user to input a file path to an old canvas design.
        :return: None
        """
        open_popup.OpenPopup(self.main_window, self.log)

    @staticmethod
    def open_readme():
        """
        Open a new browser tab to the most recent version of the README on GitHub.
        :return: None
        """
        webbrowser.open_new_tab('https://github.com/mcgridles/neuromatic/blob/master/README.md')
