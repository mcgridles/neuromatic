import tkinter as tk

DEFAULT_CANVAS_NAME = 'new_canvas_{}'.format(1)
DEFAULT_CANVAS_PROPERTIES = {
    'canvas_name': DEFAULT_CANVAS_NAME,
    'component_slots': 3,
    'project_directory': '~/Documents',
    'training_size': .5
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
                 sticky='nsew',
                 logger=None,
                 main_window=None):
        self.frame = tk.Frame(root, height=size_y, width=size_x, bg='gray', padx=3, pady=3)
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

    def get_properties(self):
        return self.box_properties


class CanvasPropertiesBox(PropertiesBox):

    def __init__(self,
                 root,
                 frame_row=0,
                 frame_col=0,
                 size_x=200,
                 size_y=200,
                 sticky='nsew',
                 logger=None):

        super(CanvasPropertiesBox, self).__init__(root,
                                                  frame_row=frame_row,
                                                  frame_col=frame_col,
                                                  size_x=size_x,
                                                  size_y=size_y,
                                                  sticky=sticky,
                                                  label_name='CanvasPropertiesBox',
                                                  init_properties=DEFAULT_CANVAS_PROPERTIES,
                                                  logger=None)



class LayerPropertiesBox(PropertiesBox):

    def __init__(self,
                 root,
                 frame_row=0,
                 frame_col=0,
                 size_x=200,
                 size_y=200,
                 sticky='nsew',
                 logger=None,
                 main_window=None):

        super(LayerPropertiesBox, self).__init__(root,
                                                 frame_row=frame_row,
                                                 frame_col=frame_col,
                                                 size_x=size_x,
                                                 size_y=size_y,
                                                 sticky=sticky,
                                                 label_name='Empty Layer',
                                                 init_properties=None ,
                                                 logger=None,
                                                 main_window=None)

        self.prop_box.bind('<<Inherit>>', self.inherit_layer_type)
        self.box_label.bind('<<Inherit>>', self.inherit_layer_type)
        self.frame.bind('<<Inherit>>', self.inherit_layer_type)
        self.log = logger
        self.main_window = main_window

        self.layer_type = 'Empty'
        self.size = 1
        self.activation = 'sigmoid'
        self.dropout = .5

        self.box_properties = self.get_slot_attributes_for_text()
        self.update_text()

        self.frame.bind('<Button-1>', self.on_start)
        self.box_label.bind('<Button-1>', self.on_start)
        self.prop_box.bind('<Button-1>', self.on_start)

        self.frame.configure(cursor='hand2')
        self.box_label.configure(cursor='hand2')
        self.prop_box.configure(cursor='hand2')

        self.frame.bind('<B1-Motion>', self.on_drag)
        self.box_label.bind('<B1-Motion>', self.on_drag)
        self.prop_box.bind('<B1-Motion>', self.on_drag)

        self.frame.bind('<ButtonRelease-1>', self.on_drop)
        self.box_label.bind('<ButtonRelease-1>', self.on_drop)
        self.prop_box.bind('<ButtonRelease-1>', self.on_drop)

    def on_start(self,event):
        pass

    def on_drag(self,event):
        pass

    def on_drop(self, event):
        x, y = self.frame.winfo_pointerx(), self.frame.winfo_pointery()
        target = event.widget.winfo_containing(x, y)
        print(str(target))
        print('.!frame2.!frame.!label')
        if str(target) == '.!frame2.!frame.!label':
            self.clear_slot_attributes()

    def update_properties(self, event):
        #TODO: This is where the popup will go
        pass

    def edit_slot_attributes(self, new_layer_type=None, new_size=None, new_activation=None, new_dropout=None):
        if new_layer_type:
            self.layer_type = new_layer_type
        if new_size:
            self.size = new_size
        if new_activation:
            self.activation = new_activation
        if new_dropout:
            self.dropout = new_dropout
        if not self.layer_type:
            self.layer_type = 'Empty'
        self.box_properties = self.get_slot_attributes_for_text()
        self.update_text()

    def get_slot_attributes_for_text(self):

        if self.layer_type == 'Empty':
            return {}
        elif self.layer_type == 'Dropout':
            return {'percentage':self.dropout}
        else:
            return {'size':self.size,'activation':self.activation}


    def get_attributes(self):
        if self.layer_type == 'Empty':
            return {'Empty'}
        elif self.layer_type == 'Dropout':
            return {'Dropout Layer':{'percentage':self.dropout}}
        else:
            return {self.layer_type:{'size':self.size,'activation':self.activation}}

    def inherit_layer_type(self, event):
        #Called when button is dropped
        clt = self.main_window.current_layer_type
        if clt != 'Empty':
            self.layer_type = clt
            self.main_window.current_layer_type = 'Empty'
            self.box_label.config(text=clt + ' Layer')
            self.box_properties = self.get_slot_attributes_for_text()
            self.update_text()

    def clear_slot_attributes(self):
        self.box_label.config(text='Empty Layer')
        self.edit_slot_attributes('Empty',1,'sigmoid',.5)



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
