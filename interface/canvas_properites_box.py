import tkinter as tk


DEFAULT_CANVAS_NAME = 'new_canvas_{}'.format(1)
DEFAULT_CANVAS_PROPERTIES = {
    'canvas_name': DEFAULT_CANVAS_NAME,
    'component_slots': 3,
    'project_directory': '~/Documents',
    'training_size': .5
}
DEFAULT_LAYER_PROPERTIES = {
    'layer_type': 'DEFAULT',
    'layer_size': 100,
    'activation_function': 'sigmoid'
}


def callback(event):
    print("clicked at", event.x, event.y)


class PropertiesBox(object):

    def __init__(self,
                 root,
                 label_name,
                 init_properties,
                 frame_row=0,
                 frame_col=0,
                 size_x=200,
                 size_y=200,
                 sticky='nsew'):

        self.frame = tk.Frame(root, height=size_y, width=size_x, padx=3, pady=3)
        self.frame.grid(row=frame_row, column=frame_col, sticky=sticky)
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.grid_propagate(0)

        # Box label attached to the box
        self.box_label = tk.Label(self.frame, text=label_name, font='Helvetica 12 bold')
        self.box_label.grid(row=0, column=0, sticky='w')

        self.box_properties = init_properties

        self.prop_box = None
        self.prop_box_text = None

        # self.create_button()
        self.create_text()

        self.editor = None

    def create_button(self):
        self.prop_box_text = tk.StringVar()
        self.prop_box_text.set('Here I Am')
        self.prop_box = tk.Button(self.frame, textvariable=self.prop_box_text, command=callback)

        self.prop_box.grid(row=1, column=0, sticky='nsew')

        self.set_button_text()

    def set_button_text(self):
        new_text = ''
        for key in self.box_properties:
            new_text += ('{}:\n'.format(key))
            new_text += '   {}\n'.format(self.box_properties[key])

        self.prop_box_text.set(new_text)

    def create_text(self):
        self.prop_box = tk.Text(self.frame, padx=3, pady=3)
        self.prop_box.grid(row=1, column=0, sticky='nsew')

        self.prop_box.config(state=tk.DISABLED)
        self.prop_box.tag_configure('boldline', font='helvetica 10 bold')
        self.update_text()

        self.frame.bind('<Double-Button-1>', self.update_properties)
        self.box_label.bind('<Double-Button-1>', self.update_properties)
        self.prop_box.bind('<Double-Button-1>', self.update_properties)

    def update_properties(self, event):
        self.editor = DummyPropertiesEditor(self.frame)
        print(self.editor.data)

    def update_text(self):
        self.prop_box.config(state=tk.NORMAL)
        self.prop_box.delete('1.0', tk.END)

        if self.box_properties:
            for key in self.box_properties:
                self.prop_box.insert(tk.END, '{}:\n'.format(key), 'boldline')
                self.prop_box.insert(tk.END, '   {}\n'.format(self.box_properties[key]))

        else:
            pass

        self.prop_box.config(state=tk.DISABLED)


class CanvasPropertiesBox(PropertiesBox):

    def __init__(self,
                 root,
                 frame_row=0,
                 frame_col=0,
                 size_x=200,
                 size_y=200,
                 sticky='nsew'):

        super(CanvasPropertiesBox, self).__init__(root,
                                                  frame_row=frame_row,
                                                  frame_col=frame_col,
                                                  size_x=size_x,
                                                  size_y=size_y,
                                                  sticky=sticky,
                                                  label_name='CanvasPropertiesBox',
                                                  init_properties=DEFAULT_CANVAS_PROPERTIES)


class LayerPropertiesBox(PropertiesBox):

    def __init__(self,
                 root,
                 frame_row=0,
                 frame_col=0,
                 size_x=200,
                 size_y=200,
                 sticky='nsew'):

        super(LayerPropertiesBox, self).__init__(root,
                                                 frame_row=frame_row,
                                                 frame_col=frame_col,
                                                 size_x=size_x,
                                                 size_y=size_y,
                                                 sticky=sticky,
                                                 label_name='LayerPropertiesBox',
                                                 init_properties=None)

        self.prop_box.bind('<<Inherit>>', self.inherit_layer_type)
        self.box_label.bind('<<Inherit>>', self.inherit_layer_type)
        self.frame.bind('<<Inherit>>', self.inherit_layer_type)

    def inherit_layer_type(self, event):
        # global Layer_Type
        # if Layer_Type != 'Blank':
        #     self.layer_type = Layer_Type
        #     Layer_Type = 'Blank'
        #     self.box_label.config(text=Layer_Type)
        # else:
        #     #TODO This is where you will put the pop up call and function
        #     pass
        self.box_properties = {'testing': 'I WORK!!!'}
        self.update_text()



class DummyPropertiesEditor(object):

    def __init__(self, root):
        self.data = 'DEFAULT'

        self.dummy = tk.Toplevel(root)
        self.dummy.rowconfigure(0, weight=1)
        self.dummy.columnconfigure(0, weight=1)
        self.text = tk.Text(self.dummy, height=1, width=10)
        self.text.grid(row=0, column=0, sticky='nsew')
        self.text.insert(tk.END, self.data)

        self.button = tk.Button(self.dummy, command=self.get_text, text='OK')
        self.button.grid(row=1, column=1)

        root.wait_window(self.dummy)

    def get_text(self):
        self.data = self.text.get('1.0', tk.END)
        self.dummy.destroy()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('PropertiesBox Test')
    root.geometry('400x400')

    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    CanvasPropertiesBox(root, frame_row=0, frame_col=0)

    blank_frame_1 = tk.Frame(root, bg='blue', height=200, width=200, pady=3, padx=3)
    blank_frame_1.grid(row=0, column=1, sticky='nsew')

    blank_frame_2 = tk.Frame(root, bg='cyan', height=200, width=200, pady=3, padx=3)
    blank_frame_2.grid(row=1, column=0, sticky='nsew')

    LayerPropertiesBox(root, frame_row=1, frame_col=1)

    root.mainloop()
