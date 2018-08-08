import tkinter as tk
import canvas_properites_box, trash_icon



def callback(event):
    print("clicked at", event.x, event.y)


class CanvasFrame(object):

    def __init__(self,
                 root,
                 frame_row=0,
                 frame_col=0,
                 size_x=200,
                 size_y=200,
                 sticky='nsew',
                 logger=None,
                 main_window=None):
        self.canvas_properties_box = None
        self.trash_icon = None
        self.slots = list()
        self.log = logger
        self.root = root
        self.main_window = main_window

        self.frame = tk.Frame(root, height=size_y, width=size_x, padx=3, pady=3)
        self.frame.grid(row=frame_row, column=frame_col, sticky=sticky)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)

        self.frame.columnconfigure(1, weight=0)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=1)
        self.frame.columnconfigure(4, weight=1)
        self.frame.columnconfigure(5, weight=1)
        self.frame.columnconfigure(6, weight=1)

        self.init_default_cavnas()

    def init_default_cavnas(self):
        self.canvas_properties_box = canvas_properites_box.CanvasPropertiesBox(self.frame,
                                                                               frame_row=1,
                                                                               frame_col=1,
                                                                               logger=self.log,
                                                                               main_window=self.main_window,
                                                                               canvas_frame = self)
        self.trash_icon = trash_icon.TrashIcon(self.frame,
                                               callback,
                                               frame_row=3,
                                               frame_col=0)

        for slot_number in range(3):
            self.add_slot()


    def add_slot(self):
        print('called')
        new_col = len(self.slots) + 3
        new_layer_box = canvas_properites_box.LayerPropertiesBox(self.frame,
                                                                 frame_row=2,
                                                                 frame_col=new_col,
                                                                 size_x=100,
                                                                 size_y=200,
                                                                 logger=self.log,
                                                                 main_window=self.main_window)

        self.slots.append(new_layer_box)

    def remove_slot(self):
        box = self.slots.pop()
        box.frame.destroy()

    def get_all_slot_attributes(self):
        slot_info_list = list()
        for slot in self.slots:
            slot_info_list.append(slot.get_attributes())
        layer_information = {'layers':slot_info_list}
        return layer_information

    def get_all_project_properties(self):
        props = self.canvas_properties_box.get_properties()
        props.update(self.get_all_slot_attributes())
        return props

    def clear_slots(self):
        for slot in self.slots:
            slot.clear_slot_attributes()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('CanvasFrame Test')
    root.geometry('400x400')

    # root.rowconfigure(0, weight=0)
    root.rowconfigure(1, weight=1)

    root.columnconfigure(0, weight=1)
    # root.columnconfigure(1, weight=1)

    blank_frame_1 = tk.Frame(root, bg='blue', height=200, pady=3, padx=3)
    blank_frame_1.grid(row=0, column=0, columnspan=2, sticky='nsew')

    blank_frame_2 = tk.Frame(root, bg='cyan', width=200, pady=3, padx=3)
    blank_frame_2.grid(row=1, column=1, sticky='nsew')

    CanvasFrame(root, frame_row=1, frame_col=1)

    root.mainloop()
