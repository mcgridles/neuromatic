import tkinter as tk
import os
from abc import ABC, abstractmethod

DEFAULT_CANVAS_NAME = 'new_canvas_{}'.format(1)
DEFAULT_CANVAS_PROPERTIES = {
    'canvas_name': DEFAULT_CANVAS_NAME,
    'component_slots': 3,
    'data_path': 'None',
    'project_directory': os.path.dirname(os.path.realpath(__file__)),
    'training_size': .5,
    'optimizer': 'sgd',
    'loss': 'mean_squared_error',
    'epochs': 1
}


def is_integer(string_input):
    '''
    Simple function that determines if a value in the form of a string is a integer or not.
    Used in property editing to determine valid input.
    Works by trying to convert it to an int using a native conversion function through python, and returning true if it
    works and false if it doesn't
    :param string_input:
    :return:
    '''
    try:
        int(string_input)
        return True
    except ValueError:
        return False


def is_float(string_input):
    '''
    Simple function that determines if a value in the form of a string is a float or not.
    Used in property editing to determine valid input.
    Works by trying to convert it to an float using a native conversion function through python, and returning true if it
    works and false if it doesn't
    :param string_input:
    :return:
    '''
    try:
        float(string_input)
        return True
    except ValueError:
        return False

class PropertiesBox(object):
    def __init__(self,
                 root,
                 label_name,
                 init_properties,
                 frame_row=0,
                 frame_col=0,
                 size_x=200,
                 size_y=200,
                 sticky='nsew',
                 logger=None,
                 main_window=None,
                 canvas_frame=None):
        self.frame = tk.Frame(root, height=size_y, width=size_x, bg='gray', padx=3, pady=3)
        self.frame.grid(row=frame_row, column=frame_col, sticky=sticky)
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.grid_propagate(0)

        # Box label attached to the box
        self.box_label = tk.Label(self.frame, text=label_name, font='Helvetica 12 bold')
        self.box_label.grid(row=0, column=0, sticky='ew')

        self.box_properties = init_properties

        self.prop_box = None
        self.prop_box_text = None

        # self.create_button()
        self.create_text()

        self.editor = None

    def create_button(self):
        self.prop_box_text = tk.StringVar()
        self.prop_box_text.set('Here I Am')
        self.prop_box = tk.Button(self.frame, textvariable=self.prop_box_text, command=callback)

        self.prop_box.grid(row=1, column=0, sticky='nsew')

        self.set_button_text()

    def set_button_text(self):
        new_text = ''
        for key in self.box_properties:
            new_text += ('{}:\n'.format(key))
            new_text += '   {}\n'.format(self.box_properties[key])

        self.prop_box_text.set(new_text)

    def create_text(self):
        self.prop_box = tk.Text(self.frame, padx=3, pady=3)
        self.prop_box.grid(row=1, column=0, sticky='nsew')

        self.prop_box.config(state=tk.DISABLED)
        self.prop_box.tag_configure('boldline', font='helvetica 10 bold')
        self.update_text()

        self.frame.bind('<Double-Button-1>', self.update_properties)
        self.box_label.bind('<Double-Button-1>', self.update_properties)
        self.prop_box.bind('<Double-Button-1>', self.update_properties)

    def update_properties(self, event):
        # self.editor = DummyPropertiesEditor(self.frame)
        pass

    def update_text(self):
        self.prop_box.config(state=tk.NORMAL)
        self.prop_box.delete('1.0', tk.END)

        if self.box_properties:
            for key in self.box_properties:
                self.prop_box.insert(tk.END, '{}:\n'.format(key), 'boldline')
                self.prop_box.insert(tk.END, '   {}\n'.format(self.box_properties[key]))

        else:
            pass

        self.prop_box.config(state=tk.DISABLED)

    def get_properties(self):
        return self.box_properties


class CanvasPropertiesBox(PropertiesBox):

    def __init__(self,
                 root,
                 frame_row=0,
                 frame_col=0,
                 size_x=200,
                 size_y=200,
                 sticky='nsew',
                 logger=None,
                 main_window=None,
                 canvas_frame=None):

        super(CanvasPropertiesBox, self).__init__(root,
                                                  frame_row=frame_row,
                                                  frame_col=frame_col,
                                                  size_x=size_x,
                                                  size_y=size_y,
                                                  sticky=sticky,
                                                  label_name='CanvasPropertiesBox',
                                                  init_properties=DEFAULT_CANVAS_PROPERTIES,
                                                  logger=None,
                                                  main_window=None,
                                                  canvas_frame=None)

        self.log = logger
        self.main_window = main_window
        if canvas_frame:
            self.canvas_frame = canvas_frame

        self.frame.bind('<Double-Button-1>', self.edit_popup)
        self.box_label.bind('<Double-Button-1>', self.edit_popup)
        self.prop_box.bind('<Double-Button-1>', self.edit_popup)

    def edit_popup(self, event):
        popup = CanvasProperties(self,main_window=self.main_window, logger=self.log,canvas_frame=self.canvas_frame)

    def edit_canvas_attributes(self, new_canvas_name=None, new_slot_count=None, new_data_path=None,
                               new_project_dir=None, new_training_size=None, new_optimizer=None, new_loss=None, new_epochs=None, old_count=None):
        self.box_properties['canvas_name'] = new_canvas_name
        self.box_properties['component_slots'] = new_slot_count
        self.box_properties['data_path'] = new_data_path
        self.box_properties['project_directory'] = new_project_dir
        self.box_properties['training_size'] = new_training_size
        self.box_properties['optimizer'] = new_optimizer
        self.box_properties['loss'] = new_loss
        self.box_properties['epochs'] = new_epochs
        self.update_text()
        self.update_slots(old_count)

    def update_slots(self,old_count):
        new_count = self.box_properties['component_slots']
        if int(old_count) > int(new_count):
            for x in range(0, int(old_count)-int(new_count)):
                self.canvas_frame.remove_slot()
        elif int(old_count) < int(new_count):
            for x in range(0, int(new_count)-int(old_count)):
                self.canvas_frame.add_slot()


class LayerPropertiesBox(PropertiesBox):

    def __init__(self,
                 root,
                 frame_row=0,
                 frame_col=0,
                 size_x=200,
                 size_y=200,
                 sticky='nsew',
                 logger=None,
                 main_window=None):

        super(LayerPropertiesBox, self).__init__(root,
                                                 frame_row=frame_row,
                                                 frame_col=frame_col,
                                                 size_x=size_x,
                                                 size_y=size_y,
                                                 sticky=sticky,
                                                 label_name='Empty Layer',
                                                 init_properties=None ,
                                                 logger=None,
                                                 main_window=None)

        self.prop_box.bind('<<Inherit>>', self.inherit_layer_type)
        self.box_label.bind('<<Inherit>>', self.inherit_layer_type)
        self.frame.bind('<<Inherit>>', self.inherit_layer_type)
        self.log = logger
        self.main_window = main_window

        self.layer_type = 'Empty'
        self.size = 1
        self.activation = 'sigmoid'
        self.dropout = .5
        self.layer_dimensions = 1

        self.box_properties = self.get_slot_attributes_for_text()
        self.update_text()

        self.frame.bind('<Button-1>', self.on_start)
        self.box_label.bind('<Button-1>', self.on_start)
        self.prop_box.bind('<Button-1>', self.on_start)

        self.frame.configure(cursor='hand2')
        self.box_label.configure(cursor='hand2')
        self.prop_box.configure(cursor='hand2')

        self.frame.bind('<B1-Motion>', self.on_drag)
        self.box_label.bind('<B1-Motion>', self.on_drag)
        self.prop_box.bind('<B1-Motion>', self.on_drag)

        self.frame.bind('<ButtonRelease-1>', self.on_drop)
        self.box_label.bind('<ButtonRelease-1>', self.on_drop)
        self.prop_box.bind('<ButtonRelease-1>', self.on_drop)

        self.frame.bind('<Double-Button-1>', self.edit_popup)
        self.box_label.bind('<Double-Button-1>', self.edit_popup)
        self.prop_box.bind('<Double-Button-1>', self.edit_popup)

    def edit_popup(self, event):
        if self.layer_type == 'Empty':
            self.log('Cannot Edit Empty Layer')
        else:
            popup = LayerProperties(self)

    def on_start(self,event):
        pass

    def on_drag(self,event):
        self.frame.configure(cursor='middlebutton')
        self.box_label.configure(cursor='middlebutton')
        self.prop_box.configure(cursor='middlebutton')
        pass

    def on_drop(self, event):
        self.frame.configure(cursor='hand2')
        self.box_label.configure(cursor='hand2')
        self.prop_box.configure(cursor='hand2')
        x, y = self.frame.winfo_pointerx(), self.frame.winfo_pointery()
        target = event.widget.winfo_containing(x, y)
        if str(target) == '.!frame2.!frame.!label':
            self.clear_slot_attributes()

    def update_properties(self, event):
        #TODO: This is where the popup will go
        pass

    def edit_slot_attributes(self, new_layer_type=None, new_size=None, new_activation=None, new_dropout=None, new_layer_dimensions=None):
        if new_layer_type:
            self.layer_type = new_layer_type
        if new_size:
            self.size = new_size
        if new_activation:
            self.activation = new_activation
        if new_dropout:
            self.dropout = new_dropout
        if new_layer_dimensions:
            self.layer_dimensions = new_layer_dimensions
        if not self.layer_type:
            self.layer_type = 'Empty'
        self.box_properties = self.get_slot_attributes_for_text()
        self.update_text()

    def get_slot_attributes_for_text(self):
        if self.layer_type == 'Empty':
            return {}
        elif self.layer_type == 'Dropout':
            return {'percentage':self.dropout}
        elif self.layer_type == 'Input':
            return {'dimensions':self.layer_dimensions}
        else:
            return {'size':self.size,'activation':self.activation}


    def get_attributes(self):
        if self.layer_type == 'Empty':
            return {'type':'empty'}
        elif self.layer_type == 'Dropout':
            return {'type':'dropout','percentage':self.dropout}
        elif self.layer_type == 'Input':
            return {'type':'input','dimensions':self.layer_dimensions}
        elif self.layer_type == 'Hidden':
            return {'type':'hidden','size':self.size,'activation':self.activation}
        elif self.layer_type == 'Output':
            return {'type':'output','size':self.size,'activation':self.activation}

    def inherit_layer_type(self, event):
        #Called when button is dropped
        clt = self.main_window.current_layer_type
        if clt != 'Empty':
            self.layer_type = clt
            self.main_window.current_layer_type = 'Empty'
            self.box_label.config(text=clt + ' Layer')
            self.box_properties = self.get_slot_attributes_for_text()
            self.update_text()

    def clear_slot_attributes(self):
        self.box_label.config(text='Empty Layer')
        self.edit_slot_attributes('Empty',1,'sigmoid',.5)


class PropertiesEditor(ABC):
    def __init__(self, props, logger=None, main_window=None, canvas_frame=None):
        '''
        Abstract class to represent a generic property editor popup.
        :param props:
        :param logger:
        :param main_window:
        :param canvas_frame:
        '''

        # Constructs props, the dictionary of all the properties, as well as logger, main_window, and canvas_frame for some information relating to the canvas state.
        self.props = props
        self.logger = logger
        self.main_window = main_window
        self.canvas_frame = canvas_frame

        #Creates the error entry sections as it is common for layer and canvas properties
        self.error_entry = None
        self.error_mes = tk.StringVar()

        #Constructs the frame and the window root used
        self.top_frame = None
        self.root = tk \
            .Toplevel()
        self.root.title("Edit Properties")

        #Launch the functions to configure the window and frame and add the elements on the window
        self.config_frames()
        self.add_widgets()

        #Launch the abstract base class' constructor
        super().__init__()

    def config_frames(self):
        '''
        Configure the grid used to place the frame on the window, and create the frame and the grid on the frame used to
        place the elements on the frame
        :return:
        '''
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.top_frame = tk.Frame(self.root, pady=1)
        self.top_frame.grid(row=0, columnspan=2, sticky=(tk.N, tk.W, tk.E, tk.S))

    @abstractmethod
    def add_widgets(self):
        '''
        Declare an abstract method that will add the widgets to the frame
        '''
        pass

    @abstractmethod
    def save_configurations(self):
        '''Declare an abstract method that will save the new properties and close the window'''
        pass


class CanvasProperties(PropertiesEditor):
    def __init__(self, props, logger=None, main_window=None, canvas_frame=None):
        '''
        A child class of Properties Editor for editing canvas properties. This builds the widgets related to canvas
        properties, including the error notfication bar and save and close buttons.
        :param props:
        :param logger:
        :param main_window:
        :param canvas_frame:
        '''

        #Retrieve the following canvas properties from the class' dictonary passed
        self.canvas_name = props.box_properties['canvas_name']
        self.slot_count = props.box_properties['component_slots']
        self.data_path = props.box_properties['data_path']
        self.project_dir = props.box_properties['project_directory']
        self.training_size = props.box_properties['training_size']
        self.optimizer = props.box_properties['optimizer']
        self.loss = props.box_properties['loss']
        self.epochs = props.box_properties['epochs']

        #Declare all the entry widgets used in the window
        self.canvas_name_entry = None
        self.slot_count_entry = None
        self.data_path_entry = None
        self.project_dir_entry = None
        self.training_size_entry = None
        self.optimizer_entry = None
        self.loss_entry = None
        self.epochs_entry = None

        #As optimizer and loss are dropdowns, the available choices must be defined as lists and variables made for the current selection
        self.optimizers = ['sgd', 'adam', 'adagrad', 'rmsprop', 'adadelta', 'adamax', 'nadam']
        self.optimizer_selected = tk.StringVar()
        self.losses = ['mean_squared_error', 'mean_absolute_error', 'mean_absolute_percentage_error',
                       'mean_squared_logarithmic_error', 'squared_hinge', 'hinge', 'categorical_hinge', 'logcosh',
                       'categorical_crossentropy', 'sparse_categorical_crossentropy', 'binary_crossentropy',
                       'kullback_leibler_divergence', 'poisson', 'cosine_proximity']
        self.loss_selected = tk.StringVar()

        #Define a file path for the program to fall back on if the browser is launched without a valid path
        self.FILE_PATH = os.path.dirname(os.path.realpath(__file__))

        #Define the configurations available to the browser selection tool
        self.VALID_TYPES = {
            'all': ('all files', '*'),
            'csv': ('csv', '*.csv'),
            'python': ('Python', '*.py'),
            'h5py': ('h5py', '*.h5py')
        }

        #Call the constructor of the properties editor class
        super().__init__(props, logger, main_window, canvas_frame)

    def add_widgets(self):
        '''
        This function adds all the widgets to the frame; the labels, the various entry forms, the error notification,
        and the confirm and close buttons
        :return:
        '''

        #Construct the canvas name label and the text entry widget. Insert the current canvas name into the entry widget
        tk.Label(self.top_frame, text="Canvas Name:").grid(row=0, column=0, sticky=tk.E)
        self.canvas_name_entry = tk.Entry(self.top_frame)
        self.canvas_name_entry.grid(row=0, column=1)
        self.canvas_name_entry.insert(10, self.canvas_name)

        #Construct the component slots label and the text entry widget. Insert the component slot number into the entry widget
        tk.Label(self.top_frame, text="Number of Component Slots:").grid(row=1, column=0, sticky=tk.E)
        self.slot_count_entry = tk.Entry(self.top_frame)
        self.slot_count_entry.grid(row=1, column=1)
        self.slot_count_entry.insert(10, self.slot_count)

        #Construct the training data label, the text entry, and the browse button widget. Insert the path into the entry widget
        tk.Label(self.top_frame, text="Training Data Path:").grid(row=2, column=0, sticky=tk.E)
        self.data_path_entry = tk.Entry(self.top_frame)
        self.data_path_entry.grid(row=2, column=1)
        self.data_path_entry.insert(10, self.data_path)
        tk.Button(self.top_frame, text="Browse...", command=self.get_file).grid(row=2, column=2)

        #Construct the project dir label, the text entry, and the browse button widget, Insert the path into the entry widget
        tk.Label(self.top_frame, text="Project Directory:").grid(row=3, column=0, sticky=tk.E)
        self.project_dir_entry = tk.Entry(self.top_frame)
        self.project_dir_entry.grid(row=3, column=1)
        self.project_dir_entry.insert(10, self.project_dir)
        tk.Button(self.top_frame, text="Browse...", command=self.get_directory).grid(row=3, column=2)

        #Construct the training size label and the text entry widget. Insert the size into the entry widget
        tk.Label(self.top_frame, text="Training Size:").grid(row=4, column=0, sticky=tk.E)
        self.training_size_entry = tk.Entry(self.top_frame)
        self.training_size_entry.grid(row=4, column=1)
        self.training_size_entry.insert(10, self.training_size)

        #Construct the optimizer label and the dropdown widget. Give the dropdown the list of options and the variable used to track what is selected.
        tk.Label(self.top_frame, text="Optimizer:").grid(row=5, column=0, sticky=tk.E)
        self.optimizer_entry = tk.OptionMenu(self.top_frame, self.optimizer_selected,
                                                  *self.optimizers)
        self.optimizer_selected.set(self.optimizer)
        self.optimizer_entry.grid(row=5, column=1)

        #Construct the loss lable and the dropdown widget. Give the dropdown the list of options and the variable used to track what is selected
        tk.Label(self.top_frame, text="Loss:").grid(row=6, column=0, sticky=tk.E)
        self.loss_entry = tk.OptionMenu(self.top_frame, self.loss_selected,
                                             *self.losses)
        self.loss_selected.set(self.loss)
        self.loss_entry.grid(row=6, column=1)

        #Construct the epochs label and entry widget. Set the epochs to the current entry.
        tk.Label(self.top_frame, text="Epochs:").grid(row=7, column=0, sticky=tk.E)
        self.epochs_entry = tk.Entry(self.top_frame)
        self.epochs_entry.grid(row=7, column=1)
        self.epochs_entry.insert(10, self.epochs)

        #Construct the error widget with a variable to represent the displayed text
        self.error_entry = tk.Label(self.top_frame, textvariable=self.error_mes, fg="red").grid(row=8, column=0, sticky=tk.W, columnspan=2)

        #Construct the Ok and cancel button. Bind the special save configurations function to the OK, and bind the close function to cancel button
        tk.Button(self.top_frame, text="OK", command=self.save_configurations).grid(row=8, column=2,
                                                                                               sticky=tk.E, pady=3)
        tk.Button(self.top_frame, text="Cancel", command=self.root.destroy).grid(row=8, column=3,
                                                                                        sticky=tk.W, pady=3)

    def get_file(self):
        '''
        This function initializes a browse file window and lets the user select a csv file
        :return:
        '''

        #Set the available filetypes to just csv
        file_type_list = 'csv'

        #Change the filetype into a list if applicable
        if type(file_type_list) is not list or tuple:
            file_type_list = [file_type_list]

        file_types = list()

        #Will be checked in generate script, not necessary to build net
        for file_type in file_type_list:
            assert file_type in self.VALID_TYPES, '{} is not valid file type.'.format(file_type)
            file_types.append(self.VALID_TYPES[file_type])

        #Set the inital directory to whatever was initally selected by the user
        init_dir = os.path.dirname(self.data_path)

        #If the intially selected path is not valid, default to FILE_PATH defined in the construct
        if not os.path.isdir(init_dir):
            init_dir = self.FILE_PATH

        #Launch the tkinter file browse window with the inital directory
        file_name = tk.filedialog.askopenfilename(initialdir=init_dir,
                                                           title="Choose File...",
                                                           filetypes=file_types)

        #Set the new file selected into the saved filepath
        self.data_path = file_name

        #Clear the filepath entry, insert the new one into the in the entry tool, and bring back the properties editor to the top.
        self.data_path_entry.delete(0, 'end')
        self.data_path_entry.insert(10, self.data_path)
        self.root.lift()

    def get_directory(self):
        assert os.path.isdir(self.project_dir), '{} is not a valid directory.'.format(self.project_dir)

        dir_name = tk.filedialog.askdirectory(title="Choose File...", initialdir=self.project_dir)

        self.project_dir = dir_name
        self.project_dir_entry.delete(0, 'end')
        self.project_dir_entry.insert(10, self.project_dir)
        self.root.lift()

    def save_configurations(self):
        old_count = self.slot_count
        canvas_name = self.canvas_name_entry.get()
        if len(canvas_name)<1 or len(canvas_name)>32:
            self.error_mes.set("Canvas Name should be 1 to 32 char")
            return
        self.canvas_name = canvas_name

        slot_count = self.slot_count_entry.get()
        if not is_integer(slot_count):
            self.error_mes.set("Number of slots should be an int")
            return
        if int(slot_count)<3 or int(slot_count)>10:
            self.error_mes.set("Number of slots should be 3 to 10")
            return
        self.slot_count = slot_count

        data_path = self.data_path_entry.get()
        # if not os.path.isfile(data_path):
        #     self.error_mes.set("Training data does not have valid filepath")
        #     return
        self.data_path = data_path

        project_dir = self.project_dir_entry.get()
        if not os.path.isdir(project_dir):
            self.error_mes.set("Project directory does not have a valid path")
            return
        self.project_dir = project_dir

        training_size = self.training_size_entry.get()
        if not is_float(training_size):
            self.error_mes.set("Training size should be a float")
            return
        if float(training_size)<0 or float(training_size)>1:
            self.error_mes.set("Training size should be 0 to 1")
            return
        self.training_size = training_size

        self.optimizer = self.optimizer_selected.get()

        self.loss = self.loss_selected.get()

        epochs = self.epochs_entry.get()
        if not is_integer(epochs):
            self.error_mes.set("Epochs should be an int")
            return
        if int(epochs) < 1 or int(epochs) > 50:
            self.error_mes.set("Epochs should be 1 to 50")
            return
        self.epochs = epochs

        self.props.edit_canvas_attributes(new_canvas_name=self.canvas_name,
                                        new_slot_count=self.slot_count,
                                        new_data_path=self.data_path,
                                        new_project_dir=self.project_dir,
                                        new_training_size=self.training_size,
                                        new_optimizer=self.optimizer,
                                        new_loss=self.loss,
                                        new_epochs=self.epochs,
                                        old_count=old_count)
        self.root.destroy()


class LayerProperties(PropertiesEditor):
    def __init__(self, props):
        self.layer_type = props.layer_type
        self.size = props.size
        self.layer_dimensions = props.layer_dimensions
        self.activation = props.activation
        self.dropout = props.dropout

        self.layer_size_entry=None
        self.layer_dimensions_entry = None
        self.layer_function_entry = None
        self.layer_percentage_entry = None
        self.error_entry = None

        self.layer_functions = ['softmax', 'elu', 'selu', 'softplus', 'softsign', 'tanh', 'sigmoid', 'hard_sigmoid',
                                'linear']
        self.layer_function_selected = tk.StringVar()

        super().__init__(props)

    def add_widgets(self):
        self.widget_row = 0

        if self.layer_type in ['Output','Hidden']:
            tk.Label(self.top_frame, text="Layer Size:").grid(row=self.widget_row , column=0, sticky=tk.E)
            self.layer_size_entry = tk.Entry(self.top_frame)
            self.layer_size_entry.grid(row=self.widget_row , column=1)
            self.layer_size_entry.insert(10, self.size)
            self.widget_row = self.widget_row + 1
            tk.Label(self.top_frame, text="Activation Function:").grid(row=self.widget_row, column=0, sticky=tk.E)
            self.layer_function_entry = tk.OptionMenu(self.top_frame, self.layer_function_selected,
                                                      *self.layer_functions)
            self.layer_function_selected.set(self.activation)
            self.layer_function_entry.grid(row=self.widget_row, column=1)
            self.widget_row = self.widget_row + 1

        if self.layer_type == 'Input':
            tk.Label(self.top_frame, text="Layer Dimensions:").grid(row=self.widget_row , column=0, sticky=tk.E)
            self.layer_dimensions_entry = tk.Entry(self.top_frame)
            self.layer_dimensions_entry.grid(row=self.widget_row , column=1)
            self.layer_dimensions_entry.insert(10, self.layer_dimensions)
            self.widget_row = self.widget_row + 1

        if self.layer_type == 'Dropout':
            tk.Label(self.top_frame, text="Dropout Percentage:").grid(row=self.widget_row , column=0, sticky=tk.E)
            self.layer_percentage_entry = tk.Entry(self.top_frame)
            self.layer_percentage_entry.grid(row=self.widget_row , column=1)
            self.layer_percentage_entry.insert(10, self.dropout)
            tk.Label(self.top_frame).grid(row=self.widget_row , column=2)
            self.widget_row = self.widget_row + 1

        self.error_entry = tk.Label(self.top_frame, textvariable=self.error_mes, fg="red").grid(row=self.widget_row, column=0,
                                                                                                sticky=tk.W,
                                                                                                columnspan=2)
        tk.Button(self.top_frame, text="OK", command=self.save_configurations).grid(row=self.widget_row , column=2,
                                                                                        sticky=tk.E, pady=3)
        tk.Button(self.top_frame, text="Cancel", command=self.root.destroy).grid(row=self.widget_row , column=3,
                                                                       sticky=tk.W, pady=3)

    def save_configurations(self):
        if self.layer_size_entry:
            size = self.layer_size_entry.get()
            if not is_integer(size):
                self.error_mes.set("Layer Size should be an int")
                return
            if int(size)<1 or int(size)>1000:
                self.error_mes.set("Layer Size should be 1 to 1000")
                return
            self.size = size

        if self.layer_function_selected:
            self.activation = self.layer_function_selected.get()

        if self.layer_percentage_entry:
            dropout = self.layer_percentage_entry.get()
            if not is_float(dropout):
                self.error_mes.set("Dropout Percentage should be a float")
                return
            if float(dropout)<0 or float(dropout)>1:
                self.error_mes.set("Dropout Percentage should be 0 to 1")
                return
            self.dropout = dropout

        if self.layer_dimensions_entry:
            layer_dimensions = self.layer_dimensions_entry.get()
            if not is_integer(layer_dimensions):
                self.error_mes.set("Layer Dimensions should be an int")
                return
            if int(layer_dimensions)<1 or int(layer_dimensions)>100:
                self.error_mes.set("Layer Dimensions should be 1 to 100")
                return
            self.layer_dimensions = layer_dimensions

        self.props.edit_slot_attributes(new_layer_type=self.layer_type,
                                        new_size=self.size,
                                        new_activation=self.activation,
                                        new_dropout=self.dropout,
                                        new_layer_dimensions=self.layer_dimensions)
        self.root.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('PropertiesBox Test')
    root.geometry('400x400')

    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    CanvasPropertiesBox(root, frame_row=0, frame_col=0)

    blank_frame_1 = tk.Frame(root, bg='blue', height=200, width=200, pady=3, padx=3)
    blank_frame_1.grid(row=0, column=1, sticky='nsew')

    blank_frame_2 = tk.Frame(root, bg='cyan', height=200, width=200, pady=3, padx=3)
    blank_frame_2.grid(row=1, column=0, sticky='nsew')

    LayerPropertiesBox(root, frame_row=1, frame_col=1)

    root.mainloop()
