import tkinter
import pickle
import os
import tkinter.filedialog

from backend import control
from interface import buttons, status_box, canvas_frame, canvas_properites_box


def get_screen_res():
    root = tkinter.Tk()
    root.withdraw()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()

    return width, height


def callback():
    pass


class Window(object):

    def __init__(self, title, width, height):
        self.width = width
        self.height = height

        # This will store which layer is selected
        self.current_layer_type = 'Empty'

        self.root = tkinter.Tk()
        self.root.title(title)

        self.set_size(self.width, self.height)
        self.root.minsize(400, 600)

        self.top_frame = None
        self.right_frame = None
        self.left_frame = None

        self.add_slot = None
        self.log = None
        self.create_new_canvas = None
        self.generate_nn_script = None
        self.train_model = None
        self.cancel_training = None
        self.clear_canvas = None
        self.empty_funct = None

        self.control = control.Control()

        self.config_frames()
        self.create_lambdas()
        self.add_widgets()

        self.control.init_status(self.status_box.add_text)

    def config_frames(self):
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=1)

        self.top_frame = tkinter.Frame(self.root, pady=3)
        self.top_frame.grid(row=0, columnspan=2, sticky="nsew")

        self.left_frame = tkinter.Frame(self.root, pady=3, padx=3, relief='sunken', borderwidth=5)
        self.left_frame.grid(row=1, column=0, sticky='nsew')
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(0, weight=1)

        self.right_frame = tkinter.Frame(self.root, pady=3, padx=3)
        self.right_frame.grid(row=1, column=1, sticky='nsew')
        self.right_frame.grid_rowconfigure(4, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

    def add_widgets(self):
        Menu(self.root, self, self.log)

        # TODO: Format buttons.py Locations
        buttons.GenericButton(root=self.top_frame,
                              button_label="New Canvas",
                              passed_function=self.create_new_canvas,
                              assigned_row=0,
                              assigned_col=0,
                              sticky='nsew',
                              logger=self.log)
        buttons.GenericButton(root=self.top_frame,
                              button_label="Generate Script",
                              passed_function=self.generate_nn_script,
                              assigned_row=0,
                              assigned_col=1,
                              sticky='nsew')
        buttons.GenericButton(root=self.top_frame,
                              button_label="Train Model",
                              passed_function=self.train_model,
                              assigned_row=0,
                              assigned_col=2,
                              sticky='nsew')
        buttons.GenericButton(root=self.top_frame,
                              button_label="Cancel",
                              passed_function=self.control.terminate_training,
                              assigned_row=0,
                              assigned_col=3,
                              sticky='nsew')
        buttons.GenericButton(root=self.top_frame,
                              button_label="Clear Slots",
                              passed_function=self.clear_canvas,
                              assigned_row=0,
                              assigned_col=4,
                              sticky='nsew')

        buttons.LayerButton(root=self.right_frame,
                            button_label="Input Layer",
                            passed_function=self.empty_funct,
                            layer_type='Input',
                            assigned_row=0,
                            assigned_col=0,
                            sticky='ew',
                            logger=self.log,
                            main_window=self)
        buttons.LayerButton(root=self.right_frame,
                            button_label="Hidden Layer",
                            passed_function=self.empty_funct,
                            layer_type='Hidden',
                            assigned_row=1,
                            assigned_col=0,
                            sticky='ew',
                            logger=self.log,
                            main_window=self)
        buttons.LayerButton(root=self.right_frame,
                            button_label="Dropout Layer",
                            passed_function=self.empty_funct,
                            layer_type='Dropout',
                            assigned_row=2,
                            assigned_col=0,
                            sticky='ew',
                            logger=self.log,
                            main_window=self)
        buttons.LayerButton(root=self.right_frame,
                            button_label="Output Layer",
                            passed_function=self.empty_funct,
                            layer_type='Output',
                            assigned_row=3,
                            assigned_col=0,
                            sticky='ew',
                            logger=self.log,
                            main_window=self)
        self.status_box = status_box.StatusBox(self.right_frame)
        self.status_box.frame.grid(row=4, column=0)

        self.slots = canvas_frame.CanvasFrame(self.left_frame,
                                              logger=self.log,
                                              main_window=self)

    def _log(self,message):
        self.status_box.add_text(message+'\n')

    def overwrite_properties(self,new_properties):
        # TODO: update canvas properties, insert the correct number of blocks
        old_count = self.slots.canvas_properties_box.box_properties['component_slots']
        name = new_properties['canvas_name']
        number = new_properties['component_slots']
        path = new_properties['data_path']
        dir = new_properties['project_directory']
        train = new_properties['training_size']
        opt = new_properties['optimizer']
        loss = new_properties['loss']
        ep = new_properties['epochs']
        self.slots.canvas_properties_box.edit_canvas_attributes(
                                            new_canvas_name=name,
                                            new_slot_count=number,
                                            new_data_path=path,
                                            new_project_dir=dir,
                                            new_training_size=train,
                                            new_optimizer=opt,
                                            new_loss=loss,
                                            new_epochs=ep,
                                            old_count=old_count
        )

        self.slots.canvas_properties_box.update_slots(number)

        num_slots = new_properties['component_slots']
        for x in range(0,int(num_slots)):
            layer = new_properties['layers'][x]
            if layer['type'] == 'hidden':
                self.slots.slots[x].edit_slot_attributes(
                                    new_layer_type='Hidden',
                                    new_size=layer['size'],
                                    new_activation=layer['activation'])
                self.slots.slots[x].box_label.config(text='Hidden Layer')

            if layer['type'] == 'output':
                self.slots.slots[x].edit_slot_attributes(
                                    new_layer_type='Output',
                                    new_size=layer['size'],
                                    new_activation=layer['activation'])
                self.slots.slots[x].box_label.config(text='Output Layer')

            if layer['type'] == 'input':
                self.slots.slots[x].edit_slot_attributes(
                                    new_layer_type='Input',
                                    new_layer_dimensions=layer['dimensions'])
                self.slots.slots[x].box_label.config(text='Input Layer')
            if layer['type'] == 'dropout':
                self.slots.slots[x].edit_slot_attributes(
                                    new_layer_type='Dropout',
                                    new_dropout=layer['percentage'])
                self.slots.slots[x].box_label.config(text='Dropout Layer')

    def create_lambdas(self):
        # This is where all the buttons different functions will be listed. They will be defined as lambdas so
        # that they can be passed into the buttons.py class as input arguments so the buttons.py class will remain
        # compact.
        #
        self.add_slot = lambda: (
            self.slots.append(canvas_properites_box.LayerPropertiesBox(self.canvas_frame)),
            self.slots[-1].frame.grid(row=0,column=len(self.slots)-1)
        )

        self.log = lambda message: (
            self._log(message)
        )

        self.create_new_canvas = lambda: (
            #TODO: Create New Canvas
            self.slots.clear_canvas(),
            self.log("Creating New Canvas"),
            self.status_box.clear()
        )

        self.generate_nn_script = lambda: (
            self.control.set_properties(self.slots.get_all_project_properties()),
            self.control.generate_network()
        )

        self.train_model = lambda: (
            self.control.set_properties(self.slots.get_all_project_properties()),
            self.control.train_in_new_thread()
        )

        self.clear_canvas = lambda: (
            self.log('Clearing Slots'),
            self.slots.clear_slots(),
        )

        self.empty_funct = lambda: ()

    def start(self):
        self.__get_status_updates()
        self.root.mainloop()

    def set_size(self, width, height):
        set_str = '{}x{}'.format(str(width), str(height))
        self.root.geometry(set_str)

    def __get_status_updates(self):
        """
        Checks for updates to the status box from the training process every 500ms.
        """
        status = self.control.check_pipe()
        if status:
            self.status_box.add_text(status)
        self.root.after(500, self.__get_status_updates)


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
        full_path = save_location+ '/'+ file_name + '.txt'
        with open(os.path.expanduser(full_path),'wb') as file:
            pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)

    def open(self):
        popup = OpenPopup(self.main_window, self.log)


class OpenPopup(object):
    def __init__(self, main_window,logger):
        self.FILE_PATH = os.path.dirname(os.path.realpath(__file__))
        self.root = tkinter.Toplevel()
        self.root.title('Title')
        self.data_path = os.path.expanduser('~')
        self.main_window = main_window
        self.log = logger
        self.config_frames()
        self.add_widgets()

    def config_frames(self):

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.top_frame = tkinter.Frame(self.root, pady=1)
        self.top_frame.grid(row=0, columnspan=2, sticky=('nesw'))

    def add_widgets(self):
        tkinter.Label(self.top_frame, text="File Path:").grid(row=1, column=0)
        self.data_path_entry = tkinter.Entry(self.top_frame)
        self.data_path_entry.grid(row=1, column=1)
        self.data_path_entry.insert(10, self.data_path)
        tkinter.Button(self.top_frame, text="Browse...", command=self.get_file).grid(row=1, column=2)

        tkinter.Button(self.top_frame, text="OK", command=self.save_configurations).grid(row=2, column=0,
                                                                                               sticky=tkinter.W, pady=3)
        tkinter.Button(self.top_frame, text="Cancel", command=self.root.destroy).grid(row=2, column=1,
                                                                                        sticky=tkinter.E, pady=3)

    def get_file(self):
        file_type_list = 'json'

        if type(file_type_list) is not list or tuple:
            file_type_list = [file_type_list]

        file_types = list()

        init_dir = os.path.dirname(self.data_path)

        assert os.path.isdir(init_dir), '{} is not a valid directory.'.format(init_dir)
        file_name = tkinter.filedialog.askopenfilename(initialdir=init_dir,
                                                           title="Choose File...",
                                                           filetypes=file_types)

        self.data_path = file_name
        self.data_path_entry.delete(0, 'end')
        self.data_path_entry.insert(10, self.data_path)
        self.root.lift()

    def save_configurations(self):
        self.data_path = self.data_path_entry.get()
        with open(self.data_path,'rb') as file:
            self.log('Opened ' + str(self.data_path))
            info = pickle.load(file)
            self.main_window.overwrite_properties(info)
        self.root.destroy()

    def start(self):
        self.root.mainloop()

    def set_size(self, width, height):
        set_str = '{}x{}'.format(str(width), str(height))
        self.root.geometry(set_str)

def main():
    width, height = get_screen_res()
    window = Window('Neuromatic', 800, 600)
    window.start()


if __name__ == '__main__':
    main()
