import tkinter
import pickle
import os
import buttons, status_box, canvas_frame, canvas_properites_box
import tkinter.filedialog

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

        #This will store which layer is selected
        self.current_layer_type = 'Empty'

        self.root = tkinter.Tk()
        self.root.title(title)

        self.set_size(self.width, self.height)
        self.root.minsize(800, 600)

        self.top_frame = None
        self.right_frame = None
        self.canvas_frame = None

        self.add_slot = None
        self.log = None
        self.create_new_canvas = None
        self.generate_nn_script = None
        self.train_model = None
        self.cancel_training = None
        self.clear_canvas = None
        self.empty_funct = None

        self.config_frames()
        self.create_lambdas()
        self.add_widgets()

    def config_frames(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=9)
        self.root.grid_columnconfigure(0, weight=16)
        self.root.grid_columnconfigure(1, weight=7)

        self.top_frame = tkinter.Frame(self.root, bg='white', pady=3)
        self.top_frame.grid(row=0, columnspan=3, sticky="nsew")

        self.left_frame = tkinter.Frame(self.root, bg='white', pady=3, padx=3)
        self.left_frame.grid(row=1, column=0, sticky='nsew')

        self.right_frame = tkinter.Frame(self.root, bg='white', pady=3, padx=3)
        self.right_frame.grid(row=1, column=1, sticky='nsew')

    def add_widgets(self):
        Menu(self.root, self)
        self.right_frame.rowconfigure(4, weight=1)
        self.right_frame.columnconfigure(0, weight=1)

        #TODO: Format buttons.py Locations
        new_button = buttons.GenericButton(self.top_frame, "New", self.create_new_canvas, logger=self.log)
        new_button.f.grid(row=0,column=0)
        generate_button = buttons.GenericButton(self.top_frame, "Generate", self.generate_nn_script)
        generate_button.f.grid(row=0, column=1)
        train_button = buttons.GenericButton(self.top_frame, "Train", self.train_model)
        train_button.f.grid(row=0, column=2)
        cancel_button = buttons.GenericButton(self.top_frame, "Cancel", self.cancel_training)
        cancel_button.f.grid(row=0, column=3)
        clear_button = buttons.GenericButton(self.top_frame, "Clear", self.clear_canvas)
        clear_button.f.grid(row=0, column=4)

        input_layer_button = buttons.LayerButton(self.right_frame, "Input Layer", self.empty_funct, 'Input', 0, logger=self.log, main_window=self)
        input_layer_button.f.grid(row=0,column=0)
        input_layer_button.make_draggable()
        hidden_layer_button = buttons.LayerButton(self.right_frame, "Hidden Layer", self.empty_funct, 'Hidden', 1, logger=self.log, main_window=self)
        hidden_layer_button.f.grid(row=1, column=0)
        hidden_layer_button.make_draggable()
        hidden_layer_button = buttons.LayerButton(self.right_frame, "Dropout Layer", self.empty_funct, 'Dropout', 2, logger=self.log, main_window=self)
        hidden_layer_button.f.grid(row=2, column=0)
        hidden_layer_button.make_draggable()
        output_layer_button = buttons.LayerButton(self.right_frame, "Output Layer", self.empty_funct, 'Output', 3, logger=self.log, main_window=self)
        output_layer_button.f.grid(row=3, column=0)
        output_layer_button.make_draggable()
        self.status_box = status_box.StatusBox(self.right_frame)
        self.status_box.frame.grid(row=4, column=0)

        self.slots = canvas_frame.CanvasFrame(self.left_frame,
                                 frame_row=1,
                                 frame_col=1,
                                 logger=self.log,
                                 main_window=self)

    def _log(self,message):
        self.status_box.add_text(message)

    def overwrite_properties(self,new_properties):
        # TODO: update canvas properties, insert the correct number of blocks

        # self.slots.canvas_properties_box.update_text()

        num_slots = new_properties['component_slots']
        for x in range(0,num_slots):
            layer = new_properties['layers'][x]
            if 'Hidden' in layer:
                layer = layer['Hidden']
                self.slots.slots[x].edit_slot_attributes(
                                    new_layer_type='Hidden',
                                    new_size=layer['size'],
                                    new_activation=layer['activation'])
                self.slots.slots[x].box_label.config(text='Hidden Layer')

            if 'Output' in layer:
                layer = layer['Output']
                self.slots.slots[x].edit_slot_attributes(
                                    new_layer_type='Output',
                                    new_size=layer['size'],
                                    new_activation=layer['activation'])
                self.slots.slots[x].box_label.config(text='Output Layer')

            if 'Input' in layer:
                layer = layer['Input']
                self.slots.slots[x].edit_slot_attributes(
                                    new_layer_type='Input',
                                    new_size=layer['size'],
                                    new_activation=layer['activation'],
                                    new_layer_dimensions=layer['dimensions'])
                self.slots.slots[x].box_label.config(text='Input Layer')
            if 'Dropout' in layer:
                layer = layer['Dropout']
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
            self.log("Creating New Canvas")
        )

        self.generate_nn_script = lambda: (
            #TODO: Add the generation script here
            self.log("Generating Neural Network Script"),
            print(self.slots.get_all_project_properties())
        )

        self.train_model = lambda: (
            #TODO: Add the training script call here
            self.log("Training Model")
        )

        self.cancel_training = lambda: (
            #TODO: Add the canceling functionality here
            self.log("Canceling Training\n")
        )

        self.clear_canvas = lambda: (
            self.log('Clearing Slots\n'),
            self.slots.clear_slots()
        )

        self.empty_funct = lambda: (

        )

    def start(self):
        self.root.mainloop()

    def set_size(self, width, height):
        set_str = '{}x{}'.format(str(width), str(height))
        self.root.geometry(set_str)


class Menu(object):

    def __init__(self, root, main_window):
        self.menu = tkinter.Menu(root)
        root.config(menu=self.menu)
        self.add()
        self.main_window = main_window

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
        print (data)
        with open(os.path.expanduser(full_path),'wb') as file:
            pickle.dump(data, file, protocol=pickle.HIGHEST_PROTOCOL)

    def open(self):
        popup = OpenPopup(self.main_window)



class OpenPopup(object):
    def __init__(self, main_window):
        self.FILE_PATH = os.path.dirname(os.path.realpath(__file__))
        self.root = tkinter.Toplevel()
        self.root.title('Title')
        self.data_path = os.path.expanduser('~')
        self.main_window = main_window

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
