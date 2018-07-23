import tkinter


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
        Button(self.top_frame)
        TextBox(self.right_frame)

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


class Button(object):

    def __init__(self, root):
        f = tkinter.Frame(root, height=47, width=47)
        f.pack_propagate(0)  # don't shrink
        f.pack()

        b = tkinter.Button(f, text="Sure!")
        b.pack(fill=tkinter.BOTH, expand=1)


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

