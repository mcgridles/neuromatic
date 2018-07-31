import tkinter
from buttons import *



Layer_Type = 'Blank'
Num_Layers = 3

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
        self.layer_type = None

        self.root = tkinter.Tk()
        self.root.title(title)
        self.set_size(self.width, self.height)
        self.root.minsize(800, 600)

        self.top_frame = None
        self.right_frame = None
        self.canvas_frame = None

        self.config_frames()
        self.slots = []
        self.create_lambdas()
        self.add_widgets()

    def config_frames(self):
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.top_frame = tkinter.Frame(self.root, bg='cyan', height=50, pady=3)
        self.top_frame.grid(row=0, columnspan=2, sticky="ew")

        self.right_frame = tkinter.Frame(self.root, bg='yellow', width=200, pady=3, padx=3)
        self.right_frame.grid(row=1, column=1, sticky='nse')

        self.canvas_frame = tkinter.Frame(self.root, bg='green', width=600, pady=3, padx=3)
        self.canvas_frame.grid(row=1, column=0, sticky='nsew')

    def add_widgets(self):
        Menu(self.root)

        #TODO: Format buttons.py Locations
        new_button = GenericButton(self.top_frame, "New", self.create_new_canvas)
        new_button.f.grid(row=0,column=0)
        generate_button = GenericButton(self.top_frame, "Generate", self.generate_nn_script)
        generate_button.f.grid(row=0, column=1)
        train_button = GenericButton(self.top_frame, "Train", self.train_model)
        train_button.f.grid(row=0, column=2)
        cancel_button = GenericButton(self.top_frame, "Cancel", self.cancel_training)
        cancel_button.f.grid(row=0, column=3)
        clear_button = GenericButton(self.top_frame, "Clear", self.clear_canvas)
        clear_button.f.grid(row=0, column=4)

        input_layer_button = LayerButton(self.right_frame, "Input Layer", self.empty_funct, 'Input', 0)
        input_layer_button.f.grid(row=0,column=0)
        input_layer_button.make_draggable()
        hidden_layer_button = LayerButton(self.right_frame, "Hidden Layer", self.empty_funct, 'Hidden', 1)
        hidden_layer_button.f.grid(row=1, column=0)
        hidden_layer_button.make_draggable()
        output_layer_button = LayerButton(self.right_frame, "Output Layer", self.empty_funct, 'Output', 2)
        output_layer_button.f.grid(row=2, column=0)
        output_layer_button.make_draggable()

        self.add_slot()
        self.add_slot()
        self.add_slot()

    def get_slots(self):
        for slot in self.slots:
            print(slot.get_slot_info())


    def create_lambdas(self):
        # This is where all the buttons different functions will be listed. They will be defined as lambdas so
        # that they can be passed into the buttons.py class as input arguments so the buttons.py class will remain
        # compact.

        self.add_slot = lambda: (
            self.slots.append(SlotButton(self.canvas_frame, self.empty_funct)),
            self.slots[-1].f.grid(row=0,column=len(self.slots)-1)
        )

        self.create_new_canvas = lambda: (
            print("Creating New Canvas")
        )

        self.generate_nn_script = lambda: (
            print("Generating Neural Network Script"),
            self.get_slots()
        )

        self.train_model = lambda: (
            print("Training Model")
        )

        self.cancel_training = lambda: (
            print("Canceling Training")
        )

        self.clear_canvas = lambda: (
            print("Clearing Canvas")
        )

        self.empty_funct = lambda: (
            print("No Function")
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

class TextBox(object):

    def __init__(self, root, height=10, width=10):
        frame = tkinter.Frame(root, bg='blue', height=100, pady=3, padx=3)
        frame.grid(row=1, sticky='sew')

        scroll = tkinter.Scrollbar(frame)
        text = tkinter.Text(frame, height=height, width=width)
        scroll.pack(side=tkinter.BOTTOM, fill=tkinter.Y)
        text.pack(side=tkinter.BOTTOM, fill=tkinter.Y)
        scroll.config(command=text.yview)
        text.config(yscrollcommand=scroll.set)
        quote = 'Here is some text'
        text.insert(tkinter.END, quote)

    def add_text(self, text, color):
        """
        Append text to the text box in a certain color.
        -- RED for Error
        :param text:
        :param color:
        :return:
        """
        pass


def main():
    width, height = get_screen_res()
    window = Window('test', 800, 600)
    window.start()


if __name__ == '__main__':
    main()
