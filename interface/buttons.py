import tkinter
Height = 47
Xoff = 706
Yoff = 107

def button_init():
    global Layer_Type

class GenericButton(object):
    #TODO: Format Buttons
    def __init__(self, root, button_label, passed_function, layer_type='Blank', offset=0):
        self.f = tkinter.Frame(root, height=Height, width=100)
        #TODO: CRITICAL check your personal offset. not sure how to do suitable workaround
        #but this works for now. Change when not as busy
        self.x_offset = Xoff
        self.y_offset = Yoff
        self.root = root
        self.f.pack_propagate(0)  # don't shrink
        self.f.pack()
        self.offset = offset*Height
        self.passed_function = passed_function
        self.layer_type = layer_type
        self.b = tkinter.Button(self.f, text=button_label, command=self.button_callback)
        self.b.pack(fill=tkinter.BOTH, expand=1)

    def button_callback(self):
        self.passed_function()


class LayerButton(GenericButton):
    def make_draggable(self):

        self.b.bind('<Button-1>', self.on_start)
        self.b.bind('<B1-Motion>', self.on_drag)
        self.b.bind('<ButtonRelease-1>', self.on_drop)
        self.b.configure(cursor='hand2')

    def button_callback(self):
       print("Wrong")

    def on_start(self, event):
        x,y = event.x,event.y
        global Layer_Type
        Layer_Type = 'Filled'
        print(x,y)

    def on_drag(self, event):
        # Uncomment and click->drag to top left corner and change offset values to the negative values
        # print(event.x,event.y)
        pass

    def on_drop(self, event):
        x,y = event.x + self.x_offset,event.y + self.y_offset
        print('Coords',x,y)
        print('test1',self.root.winfo_rootx(),self.root.winfo_rooty())
        print('test2', self.root.winfo_rootx(), self.root.winfo_rooty())
        target = event.widget.winfo_containing(x, y + self.offset)
        print("Target:",target)
        global Layer_Type
        Layer_Type = self.layer_type
        print(target)
        try:
            target.invoke()
        except:
            print("Didn't work")
            pass



class SlotButton(GenericButton):
    def __init__(self, root, passed_function, layer_type='Blank'):
        self.f = tkinter.Frame(root, height=Height*5, width=100)
        self.f.pack_propagate(0)  # don't shrink
        self.f.pack()
        #TODO: CRITICAL check your personal offset. not sure how to do suitable workaround
        #but this works for now. Change when not as busy
        self.x_offset = Xoff
        self.y_offset = Yoff
        self.root = root
        self.passed_function = passed_function
        self.layer_type = layer_type
        self.number = 1
        self.activation = 'sigmoid'
        self.btn_text = tkinter.StringVar()
        self.btn_text.set('Blank')
        self.b = tkinter.Button(self.f, textvariable=self.btn_text, command=self.button_callback)
        self.b.pack(fill=tkinter.BOTH, expand=True)

    def button_callback(self):
        global Layer_Type
        if Layer_Type != 'Blank':
            self.layer_type = Layer_Type
            Layer_Type = 'Blank'
            self.btn_text.set(self.layer_type)
        else:
            #TODO This is where you will put the pop up call and function
            print(self.layer_type)

    def get_slot_info(self):
        slot_info = {'layer_type':self.layer_type,
                'number':self.number,
                'activation':self.activation}
        return slot_info

    def edit_slot_info(self, number=1, activation=1):
        self.number = number
        self.activation = activation

def main():
    pass
if __name__ == '__main__':
    main()
