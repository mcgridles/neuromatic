import tkinter
import os
import pickle


class OpenPopup(object):
    def __init__(self, main_window, logger):
        self.FILE_PATH = os.path.expanduser('~')
        self.root = tkinter.Toplevel()
        self.root.title('Title')
        self.data_path = os.path.expanduser('~')
        self.main_window = main_window
        self.log = logger
        self.root.grab_set()
        self.top_frame = None
        self.data_path_entry = None
        self.config_frames()
        self.add_widgets()

    def config_frames(self):
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.top_frame = tkinter.Frame(self.root, pady=1)
        self.top_frame.grid(row=0, columnspan=2, sticky='nesw')

    def add_widgets(self):
        tkinter.Label(self.top_frame, text="File Path:").grid(row=1, column=0)
        self.data_path_entry = tkinter.Entry(self.top_frame)
        self.data_path_entry.grid(row=1, column=1)
        self.data_path_entry.insert(10, self.data_path)
        tkinter.Button(self.top_frame,
                       text="Browse...",
                       command=self.get_file).grid(row=1, column=2)
        tkinter.Button(self.top_frame,
                       text="OK",
                       command=self.save_configurations).grid(row=2, column=0, sticky=tkinter.W, pady=3)
        tkinter.Button(self.top_frame,
                       text="Cancel",
                       command=self.exit).grid(row=2, column=1, sticky=tkinter.E, pady=3)

    def get_file(self):
        file_types = [('Pickle Files','*.pkl')]
        init_dir = os.path.dirname(self.data_path)

        print(init_dir)
        assert os.path.isdir(init_dir), '{} is not a valid directory.'.format(init_dir)
        file_name = tkinter.filedialog.askopenfilename(initialdir=init_dir,
                                                       title="Choose File...",
                                                       filetypes=file_types)

        if file_name:
            self.data_path = file_name
            self.data_path_entry.delete(0, 'end')
            self.data_path_entry.insert(10, self.data_path)
        self.root.lift()

    def exit(self):
        self.root.grab_release()
        self.root.destroy()

    def save_configurations(self):
        self.data_path = self.data_path_entry.get()
        with open(self.data_path, 'rb') as file:
            self.log('Opened ' + str(self.data_path))
            info = pickle.load(file)
            self.main_window.overwrite_properties(info)
        self.root.grab_release()
        self.root.destroy()

    def start(self):
        self.root.mainloop()

    def set_size(self, width, height):
        set_str = '{}x{}'.format(str(width), str(height))
        self.root.geometry(set_str)
