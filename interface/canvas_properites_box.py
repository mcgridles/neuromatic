import tkinter as tk

DEFAULT_CANVAS_NAME = 'new_canvas_{}'.format(1)
DEFAULT_CANVAS_PROPERTIES = {
    'canvas_name': DEFAULT_CANVAS_NAME,
    'component_slots': 3,
    'project_directory': '~/Desktop',
    'training_size': .5
}

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
                 main_window=None):
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
                 main_window=None):

        super(CanvasPropertiesBox, self).__init__(root,
                                                  frame_row=frame_row,
                                                  frame_col=frame_col,
                                                  size_x=size_x,
                                                  size_y=size_y,
                                                  sticky=sticky,
                                                  label_name='CanvasPropertiesBox',
                                                  init_properties=DEFAULT_CANVAS_PROPERTIES,
                                                  logger=None,
                                                  main_window=None)



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
        self.layer_dimensions = [1,1]

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
            self.log('Cannot Edit Empty Layer\n')
        else:
            popup = LayerProperties(self)

    def on_start(self,event):
        pass

    def on_drag(self,event):
        pass

    def on_drop(self, event):
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
            return {'size':self.size,'activation':self.activation, 'dimensions':self.layer_dimensions}
        else:
            return {'size':self.size,'activation':self.activation}


    def get_attributes(self):
        if self.layer_type == 'Empty':
            return {'Empty'}
        elif self.layer_type == 'Dropout':
            return {self.layer_type: {'percentage':self.dropout}}
        elif self.layer_type == 'Input':
            return {self.layer_type: {'size': self.size, 'activation': self.activation, 'dimensions':self.layer_dimensions}}
        else:
            return {self.layer_type:{'size':self.size,'activation':self.activation}}

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


class CanvasProperties(object):
    def __init__(self, title, canvas_name, slot_count, data_path, project_dir):
        self.canvas_name = canvas_name
        self.slot_count = slot_count
        self.data_path = data_path
        self.project_dir = project_dir

        self.canvas_name_entry = None
        self.slot_count_entry = None
        self.data_path_entry = None
        self.project_dir_entry = None

        self.root = tk\
            .Toplevel()
        self.root.title(title)

        self.top_frame = None

        self.config_frames()
        self.add_widgets()

        self.FILE_PATH = os.path.dirname(os.path.realpath(__file__))
        #self.USER_HOME = os.path.expanduser('~')

        self.VALID_TYPES = {
            'all': ('all files', '*'),
            'csv': ('csv', '*.csv'),
            'python': ('Python', '*.py'),
            'h5py': ('h5py', '*.h5py')
        }

    def config_frames(self):
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.top_frame = tk.Frame(self.root, pady=1)
        self.top_frame.grid(row=0, columnspan=2, sticky=(tk.N, tk.W, tk.E, tk.S))

    def add_widgets(self):
        tk.Label(self.top_frame, text="Canvas Name:").grid(row=0, column=0)
        self.canvas_name_entry = tk.Entry(self.top_frame)
        self.canvas_name_entry.grid(row=0, column=1)
        self.canvas_name_entry.insert(10, self.canvas_name)

        tk.Label(self.top_frame, text="Number of Component Slots:").grid(row=1, column=0)
        self.slot_count_entry = tk.Entry(self.top_frame)
        self.slot_count_entry.grid(row=1, column=1)
        self.slot_count_entry.insert(10, self.slot_count)

        tk.Label(self.top_frame, text="Training Data Path:").grid(row=2, column=0)
        self.data_path_entry = tk.Entry(self.top_frame)
        self.data_path_entry.grid(row=2, column=1)
        self.data_path_entry.insert(10, self.data_path)
        tk.Button(self.top_frame, text="Browse...", command=self.get_file).grid(row=2, column=2)

        tk.Label(self.top_frame, text="Project Directory:").grid(row=3, column=0)
        self.project_dir_entry = tk.Entry(self.top_frame)
        self.project_dir_entry.grid(row=3, column=1)
        self.project_dir_entry.insert(10, self.project_dir)
        tk.Button(self.top_frame, text="Browse...", command=self.get_directory).grid(row=3, column=2)

        tk.Button(self.top_frame, text="OK", command=self.save_configurations).grid(row=4, column=2,
                                                                                               sticky=tk.W, pady=3)
        tk.Button(self.top_frame, text="Cancel", command=self.root.destroy).grid(row=4, column=3,
                                                                                        sticky=tk.E, pady=3)

    def get_file(self):
        file_type_list = 'csv'

        if type(file_type_list) is not list or tuple:
            file_type_list = [file_type_list]

        file_types = list()

        for file_type in file_type_list:
            assert file_type in self.VALID_TYPES, '{} is not valid file type.'.format(file_type)
            file_types.append(self.VALID_TYPES[file_type])

        init_dir = os.path.dirname(self.data_path)

        assert os.path.isdir(init_dir), '{} is not a valid directory.'.format(init_dir)

        file_name = tk.filedialog.askopenfilename(initialdir=init_dir,
                                                           title="Choose File...",
                                                           filetypes=file_types)

        self.data_path = file_name
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
        self.canvas_name = self.canvas_name_entry.get()
        self.slot_count = self.slot_count_entry.get()
        self.data_path = self.data_path_entry.get()
        self.project_dir = self.project_dir_entry.get()

        self.root.destroy()

    def start(self):
        self.root.mainloop()

    def set_size(self, width, height):
        set_str = '{}x{}'.format(str(width), str(height))
        self.root.geometry(set_str)


class LayerProperties(object):
    def __init__(self, props):
        self.props = props
        self.layer_type = props.layer_type
        self.size = props.size
        self.layer_dimensions = props.layer_dimensions
        self.activation = props.activation
        self.dropout = props.dropout

        self.layer_size_entry=None
        self.layer_dimensions_entry_x = None
        self.layer_dimensions_entry_y = None
        self.layer_function_entry = None
        self.layer_percentage_entry = None

        self.layer_functions = ['softmax', 'elu', 'selu', 'softplus', 'softsign', 'tanh', 'sigmoid', 'hard_sigmoid',
                                'linear']

        self.root = tk.Toplevel()
        self.root.title(self.layer_type)

        self.top_frame = None

        self.layer_function_selected = tk.StringVar(self.root)

        self.config_frames()
        self.add_widgets()

    def config_frames(self):
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.top_frame = tk.Frame(self.root, pady=1)
        self.top_frame.grid(row=0, columnspan=2, sticky=(tk.N, tk.W, tk.E, tk.S))

    def add_widgets(self):
        self.widget_row = 0

        if self.layer_type != 'Dropout':
            tk.Label(self.top_frame, text="Layer Size:").grid(row=self.widget_row , column=0)
            self.layer_size_entry = tk.Entry(self.top_frame)
            self.layer_size_entry.grid(row=self.widget_row , column=1)
            self.layer_size_entry.insert(10, self.size)
            self.widget_row = self.widget_row + 1

        if self.layer_type == 'Input':
            tk.Label(self.top_frame, text="Layer Dimensions:").grid(row=self.widget_row , column=0)
            self.layer_dimensions_entry_x = tk.Entry(self.top_frame)
            self.layer_dimensions_entry_x.grid(row=self.widget_row , column=1)
            self.layer_dimensions_entry_x.insert(10, self.layer_dimensions[0])
            self.layer_dimensions_entry_y = tk.Entry(self.top_frame)
            self.layer_dimensions_entry_y.grid(row=self.widget_row , column=2)
            self.layer_dimensions_entry_y.insert(10, self.layer_dimensions[1])
            self.widget_row = self.widget_row + 1

        if self.layer_type != 'Dropout':
            tk.Label(self.top_frame, text="Activation Function:").grid(row=self.widget_row , column=0)
            self.layer_function_entry = tk.OptionMenu(self.top_frame, self.layer_function_selected,
                                                           *self.layer_functions)
            self.layer_function_selected.set(self.activation)
            self.layer_function_entry.grid(row=self.widget_row , column=1)
            self.widget_row = self.widget_row + 1

        if self.layer_type == 'Dropout':
            tk.Label(self.top_frame, text="Percentage:").grid(row=self.widget_row , column=0)
            self.layer_percentage_entry = tk.Entry(self.top_frame)
            self.layer_percentage_entry.grid(row=self.widget_row , column=1)
            self.layer_percentage_entry.insert(10, self.dropout)
            tk.Label(self.top_frame, text="%").grid(row=self.widget_row , column=2)
            self.widget_row = self.widget_row + 1

        tk.Button(self.top_frame, text="OK", command=self.save_configurations).grid(row=self.widget_row , column=0,
                                                                                        sticky=tk.W, pady=3)
        tk.Button(self.top_frame, text="Cancel", command=self.root.destroy).grid(row=self.widget_row , column=1,
                                                                       sticky=tk.E, pady=3)
    def start(self):
        self.root.mainloop()

    def set_size(self, width, height):
        set_str = '{}x{}'.format(str(width), str(height))
        self.root.geometry(set_str)

    def save_configurations(self):
        if self.layer_size_entry:
            self.size = self.layer_size_entry.get()
        if self.layer_function_selected:
            self.activation = self.layer_function_selected.get()
        if self.layer_percentage_entry:
            self.dropout = self.layer_percentage_entry.get()
        if self.layer_dimensions_entry_x and self.layer_dimensions_entry_y:
            self.layer_dimensions = [self.layer_dimensions_entry_x.get(), self.layer_dimensions_entry_y.get()]
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
