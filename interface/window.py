import tkinter
from interface import buttons, status_box, canvas_frame, canvas_properites_box

def callback():
    print("called the callback!")


def get_screen_res():
    root = tkinter.Tk()
    root.withdraw()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()

    return width, height


class Window(object):

    def __init__(self, title, width, height):
        self.width = width
        self.height = height

        #This will store which layer is selected
        self.current_layer_type = 'Empty'

        self.root = tkinter.Tk()
        # entry = tkinter.Entry(self.root)
        # entry.pack()
        # self.root.update_idletasks()
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
        self.slots = []
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
        Menu(self.root)
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


    def get_slots(self):
        for slot in self.slots:
            print(slot.get_slot_info())

    def _log(self,message):
        self.status_box.add_text(message)

    def create_lambdas(self):
        # This is where all the buttons different functions will be listed. They will be defined as lambdas so
        # that they can be passed into the buttons.py class as input arguments so the buttons.py class will remain
        # compact.
        #
        # self.add_slot = lambda: (
        #     self.slots.append(canvas_properites_box.LayerPropertiesBox(self.canvas_frame)),
        #     self.slots[-1].frame.grid(row=0,column=len(self.slots)-1)
        # )

        self.log = lambda message: (
            self._log(message)
        )

        self.create_new_canvas = lambda: (
            print("Creating New Canvas"),
            self.slots.add_slot()

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
            self.log("Canceling Training")
        )

        self.clear_canvas = lambda: (
            self.log('Clearing Slots'),
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

    def __init__(self, root):
        self.menu = tkinter.Menu(root)
        root.config(menu=self.menu)
        self.add()

    def add(self):
        file_menu = tkinter.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=callback)
        file_menu.add_command(label="Open...", command=callback)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=callback)

        help_menu = tkinter.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About...", command=callback)


def main():
    width, height = get_screen_res()
    window = Window('Neuromatic', 800, 600)
    window.start()


if __name__ == '__main__':
    main()
