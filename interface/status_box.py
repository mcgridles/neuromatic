import tkinter


class StatusBox(object):

    def __init__(self, root, height=10, width=40):
        frame = tkinter.Frame(root, bg='blue', width=100, height=100, pady=3, padx=3)
        frame.grid(row=1, sticky='nsew')

        self.text = tkinter.Text(frame, height=height, width=width)
        self.text.config(state='disabled')
        self.text.pack(side=tkinter.LEFT, fill=tkinter.Y)

        scroll = tkinter.Scrollbar(frame)
        scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        scroll.config(command=self.text.yview)
        self.text.config(yscrollcommand=scroll.set)

    def add_text(self, text):
        """
        Append text to the text box in a certain color.
        -- RED for Error
        :param text:
        :param color:
        :return:
        """
        self.text.config(state='normal')
        self.text.insert(tkinter.END, text)
        self.text.config(state='disabled')


if __name__ == '__main__':
    root = tkinter.Tk()
    root.title('StatusBox Test')
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    button_frame = tkinter.Frame(root, bg='yellow', width=200, pady=3, padx=3)
    button_frame.grid(row=1, column=1, sticky='nsew')
    text_frame = tkinter.Frame(root, bg='green', width=600, pady=3, padx=3)
    text_frame.grid(row=1, column=0, sticky='nsew')

    box = StatusBox(text_frame)
    f = tkinter.Frame(button_frame, height=47, width=100, pady=3, padx=3)
    f.pack_propagate(0)  # don't shrink
    f.pack()

    b = tkinter.Button(f, command=lambda: box.add_text('new\n'), text="add text")
    b.pack(fill=tkinter.BOTH, expand=1)
    root.mainloop()
