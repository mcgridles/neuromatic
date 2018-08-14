import tkinter
import os
import pickle


class OpenPopup(object):

    def __init__(self, main_window, logger):
        """
        Popup dialog box used to enter the file path to a canvas design to be opened by the application.
        :param main_window: Tkinter.Tk - The main window of the application. Used to manage application data.
        :param logger: function - The function to which status strings can be passed.
        """

        # Create a new window for the dialog box
        self.root = tkinter.Toplevel()
        self.root.title('Open')
        # Get the user's home directory to use in relative paths
        self.data_path = os.path.expanduser('~')
        self.main_window = main_window
        self.log = logger
        # Freezes other windows while this window is open
        self.root.grab_set()
        self.top_frame = None
        self.data_path_entry = None
        self.config_frames()
        self.add_widgets()

    def config_frames(self):
        """
        Configure the frame positions and sizes on the window.
        :return: None
        """
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.top_frame = tkinter.Frame(self.root, pady=1)
        self.top_frame.grid(row=0, columnspan=2, sticky='nsew')

    def add_widgets(self):
        """
        Add the widgets to the window.
        :return: None
        """
        tkinter.Label(self.top_frame, text="File Path:").grid(row=1, column=0)
        self.data_path_entry = tkinter.Entry(self.top_frame)
        self.data_path_entry.grid(row=1, column=1)
        self.data_path_entry.insert(10, self.data_path)
        # Create the Browse button
        tkinter.Button(self.top_frame,
                       text="Browse...",
                       command=self.get_file).grid(row=1, column=2)
        # Create the Ok button
        tkinter.Button(self.top_frame,
                       text="OK",
                       command=self.save_configurations).grid(row=2, column=0, sticky=tkinter.W, pady=3)
        # Create the Cancel button
        tkinter.Button(self.top_frame,
                       text="Cancel",
                       command=self.exit).grid(row=2, column=1, sticky=tkinter.E, pady=3)

    def get_file(self):
        """
        Create a filedialog box that allows the user to navigate the file system using a GUI.
        :return: None
        """

        # Only look for the following file types
        file_types = [('Pickle Files', '*.pkl')]
        # The directory to which the filedialog will open by default
        init_dir = os.path.dirname(self.data_path)

        # Ensure that the init_dir is an existing directory on the file system
        assert os.path.isdir(init_dir), '{} is not a valid directory.'.format(init_dir)
        # Open the dialog box
        file_name = tkinter.filedialog.askopenfilename(initialdir=init_dir,
                                                       title="Choose File...",
                                                       filetypes=file_types)

        # If a name was chosen, update the text box
        if file_name:
            self.data_path = file_name
            self.data_path_entry.delete(0, 'end')
            self.data_path_entry.insert(10, self.data_path)
        self.root.lift()

    def exit(self):
        """
        Unfreeze root and delete the popup
        :return: None
        """
        self.root.grab_release()
        self.root.destroy()

    def save_configurations(self):
        """
        Un-serialize the data from the opened file and overwrite its properties to the current canvas properties.
        :return: None
        """
        # Get the file path
        self.data_path = self.data_path_entry.get()
        # Open the file
        with open(self.data_path, 'rb') as file:
            self.log('Opened ' + str(self.data_path))
            # Un-serialize
            info = pickle.load(file)
            # Write the new properties
            self.main_window.overwrite_properties(info)

        self.exit()

    def start(self):
        """
        Open the popup window.
        :return: None
        """
        self.root.mainloop()

    def set_size(self, width, height):
        """
        Set the size of the window.
        :param width: int - Width of the window.
        :param height: int - Height of the window.
        :return: None
        """
        # Combine the height and width to single string to be passed to root
        set_str = '{}x{}'.format(str(width), str(height))
        self.root.geometry(set_str)
