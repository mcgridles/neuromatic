import Tkinter
import toml


def callback():
    print "called the callback!"


class Window(object):

    def __init__(self, title, height=200, width=100):
        self.root = Tkinter.Tk()
        self.root.title = title
        self.set_size(height, width)

        self.add_menu()
        self.add_button()
        self.add_text_box()

    def start(self):
        self.root.mainloop()

    def set_size(self, height, width):
        set_str = '{}x{}'.format(str(height), str(width))
        self.root.geometry(set_str)

    def add_text_box(self):
        TextBox(self.root)

    def add_menu(self):
        menu = Menu(self.root)
        self.root.config(menu=menu.menu)
        menu.add()

    def add_button(self):
        Button(self.root)


class Menu(object):

    def __init__(self, root):
        self.menu = Tkinter.Menu(root)

    def add(self):
        file_menu = Tkinter.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=callback)
        file_menu.add_command(label="Open...", command=callback)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=callback)

        help_menu = Tkinter.Menu(self.menu)
        self.menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About...", command=callback)


class Button(object):

    def __init__(self, root):
        f = Tkinter.Frame(root, height=32, width=32)
        f.pack_propagate(0)  # don't shrink
        f.pack()

        b = Tkinter.Button(f, text="Sure!")
        b.pack(fill=Tkinter.BOTH, expand=1)


class TextBox(object):

    def __init__(self, root, height=10, width=10):
        scroll = Tkinter.Scrollbar(root)
        text = Tkinter.Text(root, height=height, width=width)
        scroll.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
        text.pack(side=Tkinter.LEFT, fill=Tkinter.Y)
        scroll.config(command=text.yview)
        text.config(yscrollcommand=scroll.set)
        quote = 'Here is some text'
        text.insert(Tkinter.END, quote)

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
    window = Window('test')
    window.start()


if __name__ == '__main__':
    main()

