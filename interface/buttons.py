import tkinter
Height = 47

def button_init():
    global Layer_Type

class GenericButton(object):
    #TODO: Format Buttons
    def __init__(self, root, button_label, passed_function, layer_type='Blank', assigned_row=0, assigned_col=0, logger=None):
        self.f = tkinter.Frame(root, height=Height)
        self.f.grid(sticky='nesw')
        self.root = root
        self.passed_function = passed_function
        self.layer_type = layer_type
        self.b = tkinter.Button(self.f, text=button_label, command=self.button_callback)
        self.b.grid(sticky='nesw')

    def button_callback(self):
        self.passed_function()


class LayerButton(GenericButton):
    def make_draggable(self):

        self.b.bind('<Button-1>', self.on_start)
        self.b.bind('<B1-Motion>', self.on_drag)
        self.b.bind('<ButtonRelease-1>', self.on_drop)
        self.b.configure(cursor='hand2')

    def button_callback(self):
        pass

    def on_start(self, event):
        global Layer_Type
        Layer_Type = self.layer_type

    def on_drag(self, event):
        pass

    def on_drop(self, event):
        x,y = self.root.winfo_pointerx(), self.root.winfo_pointery()
        target = event.widget.winfo_containing(x,y)
        global Layer_Type
        Layer_Type = self.layer_type
        try:
            target.invoke()
        except:
            print("Didn't work")
            pass



class SlotButton(GenericButton):
    def __init__(self, root, passed_function, layer_type='Blank'):
        self.f = tkinter.Frame(root, height=300, width=100)
        self.f.grid()
        self.root = root
        self.passed_function = passed_function
        self.layer_type = layer_type
        self.number = 1
        self.activation = 'sigmoid'
        self.btn_text = tkinter.StringVar()
        self.btn_text.set('Blank')
        self.b = tkinter.Button(self.f, textvariable=self.btn_text, command=self.button_callback)
        self.b.grid(row=0,column=0)

    def button_callback(self):
        global Layer_Type
        if Layer_Type != 'Blank':
            self.layer_type = Layer_Type
            Layer_Type = 'Blank'
            self.btn_text.set(self.layer_type)
        else:
            #TODO This is where you will put the pop up call and function
            pass

    def get_slot_info(self):
        slot_info = {self.layer_type:{'size':self.number,'activation':self.activation}}
        return slot_info

    def edit_slot_info(self, number=1, activation=1):
        self.number = number
        self.activation = activation

def main():
    pass
if __name__ == '__main__':
    main()
