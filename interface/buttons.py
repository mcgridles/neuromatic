import tkinter


HEIGHT = 47

class GenericButton(object):
    #TODO: Format Buttons
    def __init__(self,
                 root,
                 button_label,
                 passed_function,
                 assigned_row=0,
                 assigned_col=0,
                 sticky='nsew',
                 logger=None,
                 main_window=None):

        self.root = root
        self.passed_function = passed_function
        self.b = tkinter.Button(self.root, text=button_label, command=self.button_callback)
        self.b.grid(row=assigned_row, column=assigned_col, sticky=sticky)
        self.log = logger
        self.main_window = main_window

    def button_callback(self):
        self.passed_function()


class LayerButton(GenericButton):

    def __init__(self,
                 root,
                 button_label,
                 passed_function,
                 layer_type='Blank',
                 assigned_row=0,
                 assigned_col=0,
                 sticky='nsew',
                 logger=None,
                 main_window=None):

        super(LayerButton, self).__init__(root=root,
                                          button_label=button_label,
                                          passed_function=passed_function,
                                          assigned_row=assigned_row,
                                          assigned_col=assigned_col,
                                          sticky=sticky,
                                          logger=None,
                                          main_window=None)
        self.log = logger
        self.main_window = main_window
        self.layer_type = layer_type

        self.make_draggable()

    def make_draggable(self):

        self.b.bind('<Button-1>', self.on_start)
        self.b.bind('<B1-Motion>', self.on_drag)
        self.b.bind('<ButtonRelease-1>', self.on_drop)
        self.b.configure(cursor='hand2')

    def button_callback(self):
        pass

    def on_start(self, event):
        self.main_window.current_layer_type = self.layer_type

    def on_drag(self, event):
        self.b.configure(cursor='middlebutton')
        pass

    def on_drop(self, event):
        self.b.configure(cursor='hand2')
        x,y = self.root.winfo_pointerx(), self.root.winfo_pointery()
        target = event.widget.winfo_containing(x,y)
        try:
            target.event_generate('<<Inherit>>', when='tail')
        except:
            pass

def main():
    pass


if __name__ == '__main__':
    main()
