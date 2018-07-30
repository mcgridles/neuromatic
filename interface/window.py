import tkinter
from interface import *


Layer_Type = 'Blank'

def callback():
    print("called the callback!")


def get_screen_res():
    root = tkinter.Tk()
    root.withdraw()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()

    return width, height

# This is where all the buttons different functions will be listed. They will be defined as lambdas so
# that they can be passed into the button class as input arguments so the button class will remain
# compact. We can move them to the window class if thats preferable which it probably is


create_new_canvas=lambda: (
    print("Creating New Canvas")
    # TODO: Add functionality to this function (are you sure -> clear canvas components)
    )


generate_nn_script=lambda: (
    print("Generating Neural Network Script")
    # TODO: Add functionality to this function (are you sure -> clear canvas components)
    )


train_model=lambda: (
    print("Training Model")
    # TODO: Add functionality to this function (are you sure -> clear canvas components)
    )

cancel_training=lambda: (
    print("Canceling Training")
    # TODO: Add functionality to this function (are you sure -> clear canvas components)
    )
clear_canvas=lambda: (
    print("Clearing Canvas")
    # TODO: Add functionality to this function (are you sure -> clear canvas components)
    )
empty_funct=lambda: (
    print("No Function")
    )


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

        #TODO: Format Button Locations
        new_button = Button(self.top_frame, "New", create_new_canvas)
        new_button.f.grid(row=0,column=0)
        generate_button = Button(self.top_frame, "Generate", generate_nn_script)
        generate_button.f.grid(row=0, column=1)
        train_button = Button(self.top_frame, "Train", train_model)
        train_button.f.grid(row=0, column=2)
        cancel_button = Button(self.top_frame, "Cancel", cancel_training)
        cancel_button.f.grid(row=0, column=3)
        clear_button = Button(self.top_frame, "Clear", clear_canvas)
        clear_button.f.grid(row=0, column=4)

        input_layer_button = LayerButton(self.right_frame, "Input Layer", empty_funct, 'Input')
        input_layer_button.f.grid(row=0,column=0)
        input_layer_button.make_draggable()
        hidden_layer_button = LayerButton(self.right_frame, "Hidden Layer", empty_funct, 'Hidden')
        hidden_layer_button.f.grid(row=1, column=0)
        hidden_layer_button.make_draggable()
        output_layer_button = LayerButton(self.right_frame, "Output Layer", empty_funct, 'Output')
        output_layer_button.f.grid(row=2, column=0)
        output_layer_button.make_draggable()

        slot_one_button = SlotButton(self.canvas_frame, "Slot 1", empty_funct)


        # Button(self.top_frame, "Generate", generate_nn_script)
        # Button(self.top_frame, "Train", train_model)
        # Button(self.top_frame, "Cancel", cancel_training)
        # Button(self.top_frame, "Clear", clear_canvas)
        # TextBox(self.right_frame)

    def start(self):
        self.root.mainloop()

    def set_size(self, width, height):
        set_str = '{}x{}'.format(str(width), str(height))
        self.root.geometry(set_str)


class Button(object):
    #TODO: Format Buttons
    def __init__(self, root, button_label, passed_function,layer_type='Blank'):
        self.f = tkinter.Frame(root, height=47, width=47)
        #TODO: CRITICAL check your personal offset. not sure how to do suitable workaround
        #but this works for now. Change when not as busy
        self.x_offset = 1230
        self.y_offset = 101
        self.root = root
        self.f.pack_propagate(0)  # don't shrink
        self.f.pack()
        self.passed_function = passed_function
        self.layer_type = layer_type
        self.b = tkinter.Button(self.f, text=button_label, command=self.button_callback)
        self.b.pack(fill=tkinter.BOTH, expand=1)

    def button_callback(self):
        self.passed_function()


class LayerButton(Button):
    def make_draggable(self):

        self.b.bind('<Button-1>', self.on_start)
        self.b.bind('<B1-Motion>', self.on_drag)
        self.b.bind('<ButtonRelease-1>', self.on_drop)
        self.b.configure(cursor='hand2')

    def button_callback(self):
       print("Wrong")

    def on_start(self, event):
        x,y = event.x,event.y
        global Layer_Type
        Layer_Type = 'Filled'
        print(x,y)

    def on_drag(self, event):
        # Uncomment and click->drag to top left corner and change offset values to the negative values
        # print(event.x,event.y)
        pass

    def on_drop(self, event):
        x,y = event.x + self.x_offset,event.y + self.y_offset
        print('Coords',x,y)
        target = event.widget.winfo_containing(x, y)
        print("Target:",target)
        global Layer_Type
        Layer_Type = self.layer_type
        print(target)
        try:
            target.invoke()
        except:
            print("Didn't work")
            pass



class SlotButton(Button):
    def button_callback(self):
        global Layer_Type
        if Layer_Type != 'Blank':
            self.layer_type = Layer_Type
            Layer_Type = 'Blank'
            print('This is my type:', self.layer_type)
            print('This is the global type', Layer_Type)
        else:
            print(self.layer_type)

    def get_slot_info(self):
        return self.layer_type
        pass

    def edit_slot_info(self, number, activation):
        self.number = number
        self.activation = activation



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
    window = Window('test', width, height)
    window.start()


if __name__ == '__main__':
    main()
