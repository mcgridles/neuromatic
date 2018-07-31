import tkinter as tk


class StatusBox(object):

    def __init__(self, root, height=200, width=200):
        self.frame = tk.Frame(root, height=height, width=width, pady=3, padx=3)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.grid(sticky='nsew')

        self.text = tk.Text(self.frame)
        self.text.config(state=tk.DISABLED, wrap=tk.NONE)
        self.text.grid(row=0, column=0, stick='nsew')

        self.v_scroll = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.v_scroll.grid(row=0, column=1, stick='ns')
        self.v_scroll.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.v_scroll.set)

        self.h_scroll = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        self.h_scroll.grid(row=1, column=0, stick='ew')
        self.h_scroll.config(command=self.text.xview)
        self.text.config(xscrollcommand=self.h_scroll.set)

    def add_text(self, text):
        """
        Append text to the text.
        :param text: String to be added to the status box.
        :return: None
        """
        if type(text) is not str:
            raise TypeError('Value passed to add_text must be a string.')

        # Enable text edit
        self.text.config(state=tk.NORMAL)
        # Add new text to the bottom
        self.text.insert(tk.END, text)
        # Disable text edit
        self.text.config(state=tk.DISABLED)

        # Get the current position of the scroll bar
        y_position = self.v_scroll.get()
        x_position = self.h_scroll.get()
        # Continue the auto scroll if scroll bar is set to bottom
        if y_position[1] == 1.0 and x_position[0] == 0.0:
            # Scroll to the end of the text box
            self.text.see(tk.END)
            self.h_scroll.set(x_position[0], x_position[1])


if __name__ == '__main__':
    root = tk.Tk()
    root.title('StatusBox Test')
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    text_frame = tk.Frame(root, bg='green', height=200, width=200, pady=3, padx=3)
    text_frame.grid(row=0, column=0, sticky='nsew')
    text_frame.rowconfigure(0, weight=1)
    text_frame.columnconfigure(0, weight=1)
    box = StatusBox(text_frame)

    button_frame = tk.Frame(root, bg='yellow', height=200, width=200, pady=3, padx=3)
    button_frame.grid(row=0, column=1, sticky='nsew')
    button = tk.Button(button_frame, command=lambda: box.add_text('test\n'), text="add text")
    button.pack()

    root.mainloop()
