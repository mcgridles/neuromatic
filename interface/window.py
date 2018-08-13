import tkinter
import tkinter.filedialog
from backend import control
from interface import buttons, status_box, canvas_frame, menu


class Window(object):

    def __init__(self, title, width, height):
        """
        This class is used as the main window to the application. It stores all top level Tkinter objects and
        connects the GUI to the backend.
        :param title: str - Title of the application
        :param width: int - Width of the GUI
        :param height: int - Height of the GUI
        """
        # Instance of the main window
        self.root = tkinter.Tk()
        self.root.title(title)
        self.set_size(width, height)
        self.root.minsize(400, 600)

        # Currently selected layer on the canvas
        self.current_layer_type = 'Empty'

        # Top level Tkinter objects
        self.top_frame = None
        self.right_frame = None
        self.left_frame = None
        self.status_box = None
        self.canvas = None

        # Lambdas used to connect the GUI and Backend
        self.log = None
        self.create_new_canvas = None
        self.generate_nn_script = None
        self.train_model = None
        self.cancel_training = None
        self.clear_canvas = None
        self.empty_funct = None

        # Backend object
        self.control = control.Control()

        # Configure the window's Tkinter frames
        self.config_frames()

        self.create_lambdas()
        self.add_widgets()

        # Send initial status to the status box
        self.control.init_status(self.status_box.add_text)

    def config_frames(self):
        """
        Configure the window's Tkinter frames for widget organization.
        :return: None
        """
        # Manage how the frmaes will resize upon the window resizing
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=1)

        # Add the top_frame for buttons
        self.top_frame = tkinter.Frame(self.root, pady=3)
        self.top_frame.grid(row=0, columnspan=2, sticky="nsew")

        # Add the left_frame for the canvas
        self.left_frame = tkinter.Frame(self.root, pady=3, padx=3, relief='sunken', borderwidth=5)
        self.left_frame.grid(row=1, column=0, sticky='nsew')
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid_rowconfigure(0, weight=1)

        # Add the right frame for the status box and the layer buttons
        self.right_frame = tkinter.Frame(self.root, pady=3, padx=3)
        self.right_frame.grid(row=1, column=1, sticky='nsew')
        self.right_frame.grid_rowconfigure(4, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

    def add_widgets(self):
        """
        Fill the window frames with Tkinter widgets.
        :return: None
        """
        # Add a "File" menu to the top of the window
        menu.Menu(self.root, self, self.log)

        # Add the buttons to the tope_frame. Used to interface the GUI with the backend.
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

        # Add layer buttons to the right frame. Used for the drag and drop interface.
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

        # Add the status box to the right frame
        self.status_box = status_box.StatusBox(self.right_frame)
        self.status_box.frame.grid(row=4, column=0)

        # Add the canvas frame to the left frame
        self.canvas = canvas_frame.CanvasFrame(self.left_frame,
                                               logger=self.log,
                                               main_window=self)

    def overwrite_properties(self, new_properties):
        """
        Overwrite the current canvas design based on the properties contained in the passed dictionary.
        :param new_properties: dict -
        :return: None
        """
        old_count = self.canvas.canvas_properties_box.box_properties['component_slots']
        name = new_properties['canvas_name']
        num_slots = new_properties['component_slots']
        path = new_properties['data_path']
        directory = new_properties['project_directory']
        train = new_properties['training_size']
        opt = new_properties['optimizer']
        loss = new_properties['loss']
        ep = new_properties['epochs']

        # Edit the canvas properties
        self.canvas.canvas_properties_box.edit_canvas_attributes(
                                            new_canvas_name=name,
                                            new_slot_count=num_slots,
                                            new_data_path=path,
                                            new_project_dir=directory,
                                            new_training_size=train,
                                            new_optimizer=opt,
                                            new_loss=loss,
                                            new_epochs=ep,
                                            old_count=old_count
        )

        # Update the number of canvas slots based on the new properties
        self.canvas.canvas_properties_box.update_slots(num_slots)

        # Update the layer properties, for each layer, based on the properties passed in the layer list
        for index in range(0, int(num_slots)):
            # Get the layer from the list
            layer = new_properties['layers'][index]

            # If the layer is a hidden layer
            if layer['type'] == 'hidden':
                # Update the slot for the given layer
                self.canvas.slots[index].edit_slot_attributes(
                                    new_layer_type='Hidden',
                                    new_size=layer['size'],
                                    new_activation=layer['activation'])
                self.canvas.slots[index].box_label.config(text='Hidden Layer')

            if layer['type'] == 'output':
                self.canvas.slots[index].edit_slot_attributes(
                                    new_layer_type='Output',
                                    new_size=layer['size'],
                                    new_activation=layer['activation'])
                self.canvas.slots[index].box_label.config(text='Output Layer')

            if layer['type'] == 'input':
                self.canvas.slots[index].edit_slot_attributes(
                                    new_layer_type='Input',
                                    new_layer_dimensions=layer['dimensions'])
                self.canvas.slots[index].box_label.config(text='Input Layer')

            if layer['type'] == 'dropout':
                self.canvas.slots[index].edit_slot_attributes(
                                    new_layer_type='Dropout',
                                    new_dropout=layer['percentage'])
                self.canvas.slots[index].box_label.config(text='Dropout Layer')

    def create_lambdas(self):
        """
        This is where all the buttons different functions will be listed. They will be defined as lambdas so
        that they can be passed into the buttons.py class as input arguments so the buttons.py class will remain
        compact.
        :return: None
        """
        self.log = lambda message: (
            self.status_box.add_text(message + '\n')
        )

        self.create_new_canvas = lambda: (
            self.canvas.clear_canvas(),
            self.log("Creating New Canvas"),
            self.status_box.clear()
        )

        self.generate_nn_script = lambda: (
            self.control.set_properties(self.canvas.get_all_project_properties()),
            self.control.generate_network()
        )

        self.train_model = lambda: (
            self.control.set_properties(self.canvas.get_all_project_properties()),
            self.control.train_in_new_thread()
        )

        self.clear_canvas = lambda: (
            self.log('Clearing Slots'),
            self.canvas.clear_slots(),
        )

        self.empty_funct = lambda: ()

    def start(self):
        """
        Start the main window
        :return: None
        """
        # Check for updates from the backend
        self.__get_status_updates()
        # Starts the main window
        self.root.mainloop()

    def set_size(self, width, height):
        """
        Combine the height and width measurements to a str. Update the window size with the string.
        :param width: int
        :param height: int
        :return: None
        """
        set_str = '{}x{}'.format(str(width), str(height))
        self.root.geometry(set_str)

    def __get_status_updates(self):
        """
        Checks for updates to the status box from the training process every 500ms.
        """
        status = self.control.check_pipe()
        if status:
            self.status_box.add_text(status)
        # Check for backend status every 500ms
        self.root.after(500, self.__get_status_updates)


def main():
    window = Window('Neuromatic', 800, 600)
    window.start()


if __name__ == '__main__':
    main()
