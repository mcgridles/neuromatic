import tkinter as tk


class StatusBox(object):

    def __init__(self, root):
        self.frame = tk.Frame(root, pady=3, padx=3)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.grid(row=0, column=0, sticky='nsew')
        self.frame.grid_propagate(0)

        self.label = tk.Label(self.frame, text='Status', font='Helvetica 12 bold')
        self.label.grid(row=0, column=0, sticky='w')

        self.text = tk.Text(self.frame)
        self.text.config(state=tk.DISABLED, wrap=tk.NONE)
        self.text.grid(row=1, column=0, sticky='nsew')

        self.v_scroll = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.v_scroll.grid(row=1, column=1, sticky='ns')
        self.v_scroll.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.v_scroll.set)

        self.h_scroll = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        self.h_scroll.grid(row=2, column=0, sticky='ew')
        self.h_scroll.config(command=self.text.xview)
        self.text.config(xscrollcommand=self.h_scroll.set)
        self.add_text('Welcome to Neuromatic\n')

    def add_text(self, text):
        """
        Append text to the text.
        :param text: String to be added to the status box.
        :return: None
        """
        if type(text) is not str:
            raise TypeError('Value passed to add_text must be a string.')

        # Enable text edit
        self.text.config(state=tk.NORMAL, font='Helvetica 10')
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

    def clear(self):
        self.text.delete("1.0", 'End')
        self.text.destroy()
        self.text = tk.Text(self.frame)
        self.text.config(state=tk.DISABLED, wrap=tk.NONE)
        self.text.grid(row=1, column=0, sticky='nsew')

        self.v_scroll = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.v_scroll.grid(row=1, column=1, sticky='ns')
        self.v_scroll.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.v_scroll.set)

        self.h_scroll = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL)
        self.h_scroll.grid(row=2, column=0, sticky='ew')
        self.h_scroll.config(command=self.text.xview)
        self.text.config(xscrollcommand=self.h_scroll.set)

if __name__ == '__main__':
    root = tk.Tk()
    root.title('StatusBox Test')
    root.geometry('400x400')

    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    text_frame = tk.Frame(root, bg='green', height=200, width=200, pady=3, padx=3)
    text_frame.grid(row=1, column=1, sticky='nsew')
    text_frame.rowconfigure(0, weight=1)
    text_frame.columnconfigure(0, weight=1)

    button_frame = tk.Frame(root, bg='yellow', height=200, width=200, pady=3, padx=3)
    button_frame.grid(row=0, column=1, sticky='nsew')
    button_frame.rowconfigure(0, weight=1)
    button_frame.columnconfigure(0, weight=1)

    blank_frame_1 = tk.Frame(root, bg='blue', height=200, width=200, pady=3, padx=3)
    blank_frame_1.grid(row=0, column=0, sticky='nsew')

    blank_frame_2 = tk.Frame(root, bg='cyan', height=200, width=200, pady=3, padx=3)
    blank_frame_2.grid(row=1, column=0, sticky='nsew')

    box = StatusBox(text_frame)

    button = tk.Button(button_frame, command=lambda: box.add_text('test\n'), text="add text")
    button.grid(row=0, column=0)
    # button.pack()

    root.mainloop()