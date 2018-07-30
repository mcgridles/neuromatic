import tkinter


class StatusBox(object):

    def __init__(self, root, height=10, width=40):
        self.text = tkinter.Text(root, height=height, width=width)
        self.text.config(state='disabled')
        self.text.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand='yes')

        self.scroll = tkinter.Scrollbar(root)
        self.scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.scroll.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.scroll.set)

    def add_text(self, text):
        """
        Append text to the text.
        :param text: String to be added to the status box.
        :return: None
        """
        if type(text) is not str:
            raise TypeError('Value passed to add_text must be a string.')

        # Enable text edit
        self.text.config(state='normal')
        # Add new text to the bottom
        self.text.insert('end', text)
        # Disable text edit
        self.text.config(state='disabled')

        # Get the current position of the scroll bar
        position = self.scroll.get()
        # Continue the auto scroll if scroll bar is set to bottom
        if position[1] == 1.0:
            # Scroll to the end of the text box
            self.text.see('end')


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
