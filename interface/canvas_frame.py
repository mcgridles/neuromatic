import tkinter as tk
import canvas_properites_box, trash_icon
import copy
import os


def callback(event):
    pass


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
        self.h_scroll = None
        self.slots = list()

        self.log = logger
        self.main_window = main_window

        self.main_frame = tk.Frame(root, height=size_y, width=size_x, padx=3, pady=3, bg='white')
        self.main_frame.grid(row=frame_row, column=frame_col, sticky=sticky)
        # self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        # self.main_frame.grid_rowconfigure(2, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.top_frame = tk.Frame(self.main_frame, height=200, width=200)
        self.top_frame.grid(row=0, column=0, sticky='nsew')
        self.mid_frame = tk.Frame(self.main_frame)
        self.mid_frame.grid(row=1, column=0, sticky='nsew')
        self.mid_frame.grid_rowconfigure(0, weight=1)
        self.mid_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame = tk.Frame(self.main_frame, height=40, width=200)
        self.bottom_frame.grid(row=2, column=0, sticky='nsew')

        self.canvas = tk.Canvas(self.mid_frame)
        self.canvas.grid(row=0, column=0, sticky='nsew')

        self.h_scroll = tk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scroll.grid(row=3, column=0, sticky='ew')

        self.canvas.config(xscrollcommand=self.h_scroll.set)
        self.canvas.grid_rowconfigure(0, weight=1)
        self.canvas.grid_columnconfigure(0, weight=1)

        self.scrollable_frame = tk.Frame(self.canvas, padx=3, pady=3)
        self.scrollable_frame.rowconfigure(1, weight=1)
        self.scrollable_frame.rowconfigure(3, weight=1)
        self.scrollable_frame.columnconfigure(1, weight=1)
        self.scrollable_frame.columnconfigure(5, weight=1)

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')

        self.scrollable_frame.bind('<Configure>', self._on_frame_configure)
        self.canvas.bind('<Configure>', self._resize_frame)

        self.init_default_cavnas()
        self._prev_width = self.canvas.winfo_width()
        self._prev_height = self.canvas.winfo_height()

    def trigger_configure_event(self):
        self.canvas.event_generate('<Configure>', when='tail')
        self.scrollable_frame.event_generate('<Configure>', when='tail')

    def _resize_frame(self, event):
        # print('resize')
        new_canvas_width = event.width
        new_canvas_height = event.height

        if self.scrollable_frame.winfo_height() > new_canvas_height > 0 \
                and self.scrollable_frame.winfo_reqheight() > new_canvas_height:
            set_height = self.scrollable_frame.winfo_reqheight()
        elif new_canvas_height > 0:
            set_height = new_canvas_height
        else:
            set_height = None

        if self.scrollable_frame.winfo_width() > new_canvas_width\
                and self.scrollable_frame.winfo_reqwidth() > new_canvas_width:
            set_width = self.scrollable_frame.winfo_reqwidth()
        else:
            set_width = self.canvas.winfo_width()

        self.canvas.itemconfig(self.canvas_frame, height=set_height, width=set_width)

    def _on_frame_configure(self, event):
        # print('config')
        self.canvas.configure(scrollregion=self.canvas.bbox('all'), width=200, height=200)

    def init_default_cavnas(self):
        self.canvas_properties_box = canvas_properites_box.CanvasPropertiesBox(self.top_frame,
                                                                               frame_row=0,
                                                                               frame_col=0,
                                                                               logger=self.log,
                                                                               main_window=self.main_window,
                                                                               canvas_frame = self)
        self.trash_icon = trash_icon.TrashIcon(self.bottom_frame,
                                               callback,
                                               frame_row=0,
                                               frame_col=0,
                                               sticky='sw')

        for slot_number in range(3):
            self.add_slot()


        self.trigger_configure_event()

    def add_slot(self):
        new_col = len(self.slots) + 3
        new_layer_box = canvas_properites_box.LayerPropertiesBox(self.scrollable_frame,
                                                                 frame_row=2,
                                                                 frame_col=new_col,
                                                                 # size_x=100,
                                                                 # size_y=200,
                                                                 logger=self.log,
                                                                 main_window=self.main_window)

        self.scrollable_frame.columnconfigure(new_col, weight=0)
        self.scrollable_frame.columnconfigure(new_col+1, weight=1)

        self.slots.append(new_layer_box)
        self.scrollable_frame.update_idletasks()

    def remove_slot(self):
        slot_number = len(self.slots) + 2
        self.scrollable_frame.columnconfigure(slot_number, weight=1)
        self.scrollable_frame.columnconfigure(slot_number + 1, weight=0)
        box = self.slots.pop()
        box.frame.destroy()
        self.scrollable_frame.update_idletasks()

    def get_all_slot_attributes(self):
        slot_info_list = list()
        for slot in self.slots:
            slot_info_list.append(slot.get_attributes())
        layer_information = {'layers':slot_info_list}
        return layer_information

    def get_all_project_properties(self):
        props = copy.deepcopy(self.canvas_properties_box.get_properties())

        props.update(self.get_all_slot_attributes())
        return props

    def clear_slots(self):
        for slot in self.slots:
            slot.clear_slot_attributes()

    def clear_canvas(self):
        old_count = self.canvas_properties_box.box_properties['component_slots']
        self.canvas_properties_box.edit_canvas_attributes(new_canvas_name='new_canvas_{}'.format(1),
                                                          new_slot_count=3,
                                                          new_data_path='None',
                                                          new_project_dir=os.path.dirname(os.path.realpath(__file__)),
                                                          new_training_size=.5,
                                                          new_optimizer='sgd',
                                                          new_loss='mean_squared_error',
                                                          new_epochs=1,
                                                          old_count=old_count)
        self.clear_slots()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('CanvasFrame Test')
    root.geometry('800x800')
    root.minsize(200, 200)

    # root.rowconfigure(0, weight=0)
    root.rowconfigure(1, weight=1)

    root.columnconfigure(0, weight=1)
    # root.columnconfigure(1, weight=1)

    blank_frame_1 = tk.Frame(root, bg='blue', height=200, pady=3, padx=3)
    blank_frame_1.grid(row=0, column=0, columnspan=2, sticky='nsew')

    blank_frame_2 = tk.Frame(root, bg='cyan', width=200, pady=3, padx=3)
    blank_frame_2.grid(row=1, column=1, sticky='nsew')

    CanvasFrame(root, frame_row=1, frame_col=0)

    root.mainloop()
