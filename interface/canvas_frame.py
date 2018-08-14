import tkinter as tk
import copy
import os

from interface import canvas_properties_box, trash_icon


class CanvasFrame(object):

    def __init__(self,
                 root,
                 assigned_row=0,
                 assigned_col=0,
                 width=200,
                 height=200,
                 sticky='nsew',
                 logger=None,
                 main_window=None):
        """
        This class holds all tkinter widgets and canvas design properties related to the neural network created by
        the user.
        :param root: tkinter.Widget - Widget that encapsulates this class's widgets.
        :param assigned_row: int - Row on which this class's widgets will exist on the parent widget (root)
        :param assigned_col: int - Column on which this class's widgets will exist on the parent widget (root)
        :param width: int - The initial width of the CanvasFrame
        :param height: int - The initial height of the CanvasFrame
        :param sticky: str - The sides to which the CanvasFrame will adhere and expand
        :param logger: function - Function for passing strings to the status box.
        :param main_window: tkinter.Tk - main_window instance used for tracking canvas design data
        """
        # Initialize the 4 main canvas properties
        self.canvas_properties_box = None
        self.trash_icon = None
        self.h_scroll = None
        self.slots = list()

        # Make main_window and logger accessable to all widgets/functions
        self.log = logger
        self.main_window = main_window

        # Create the frame for the canvas
        self.main_frame = tk.Frame(root, height=height, width=width, padx=3, pady=3, bg='white')
        self.main_frame.grid(row=assigned_row, column=assigned_col, sticky=sticky)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Create the frame partition for the top of the canvas
        self.top_frame = tk.Frame(self.main_frame, height=200, width=200)
        self.top_frame.grid(row=0, column=0, sticky='nsew')

        # Create the frame partition for the middle of the canvas
        self.mid_frame = tk.Frame(self.main_frame)
        self.mid_frame.grid(row=1, column=0, sticky='nsew')
        self.mid_frame.grid_rowconfigure(0, weight=1)
        self.mid_frame.grid_columnconfigure(0, weight=1)

        # Create the frame partition for the bottom of the canvas
        self.bottom_frame = tk.Frame(self.main_frame, height=40, width=200)
        self.bottom_frame.grid(row=2, column=0, sticky='nsew')

        # Make the middle/slot partition a canvas
        self.canvas = tk.Canvas(self.mid_frame)
        self.canvas.grid(row=0, column=0, sticky='nsew')

        # Add a scroll bar to control the slot slide
        self.h_scroll = tk.Scrollbar(self.main_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.h_scroll.grid(row=3, column=0, sticky='ew')

        # Make the canvas scollable
        self.canvas.config(xscrollcommand=self.h_scroll.set)
        self.canvas.grid_rowconfigure(0, weight=1)
        self.canvas.grid_columnconfigure(0, weight=1)

        # Make a scrollable frame
        self.scrollable_frame = tk.Frame(self.canvas, padx=3, pady=3)
        self.scrollable_frame.rowconfigure(1, weight=1)
        self.scrollable_frame.rowconfigure(3, weight=1)
        self.scrollable_frame.columnconfigure(1, weight=1)
        self.scrollable_frame.columnconfigure(5, weight=1)

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')

        self.scrollable_frame.bind('<Configure>', self._on_frame_configure)
        self.canvas.bind('<Configure>', self._resize_frame)

        self.init_default_canvas()
        self._prev_width = self.canvas.winfo_width()
        self._prev_height = self.canvas.winfo_height()

    def trigger_configure_event(self):
        """
        Trigger the configure event that will correct the size of the slots frame for the size of the window.
        :return: None
        """
        self.canvas.event_generate('<Configure>', when='tail')
        self.scrollable_frame.event_generate('<Configure>', when='tail')

    def _resize_frame(self, event):
        """
        Assign the slot frame a new size based on the new size of the canvas.
        :param event:
        :return: None
        """
        # Get the size of the canvas passed through the event
        new_canvas_width = event.width
        new_canvas_height = event.height

        # If the slots frame is supposed to be taller than the canvas frame...
        if self.scrollable_frame.winfo_height() > new_canvas_height > 0 \
                and self.scrollable_frame.winfo_reqheight() > new_canvas_height:
            # Set the slots frame to its minimum height to display its widgets
            set_height = self.scrollable_frame.winfo_reqheight()
        # Set the new height to the height of the canvas if the new_canvas_height is changed as a result of the canvas
        # design changing. NOT as a result of the user manipulating the window size.
        elif new_canvas_height > 0:
            set_height = new_canvas_height
        else:
            set_height = None

        if self.scrollable_frame.winfo_width() > new_canvas_width\
                and self.scrollable_frame.winfo_reqwidth() > new_canvas_width:
            set_width = self.scrollable_frame.winfo_reqwidth()
        else:
            set_width = self.canvas.winfo_width()

        # Set the canvas frame's new height and width
        self.canvas.itemconfig(self.canvas_frame, height=set_height, width=set_width)

    def _on_frame_configure(self, event):
        """
        Triggered by a <Configure> event on the canvas. Changes the size of the scrollable area.
        :param event: tkinter event that triggers this method
        :return: None
        """
        self.canvas.configure(scrollregion=self.canvas.bbox('all'), width=200, height=200)

    def init_default_canvas(self):
        """
        Create a default canvas
        :return:  None
        """
        # Create a canvas properties box with default values.
        self.canvas_properties_box = canvas_properties_box.CanvasPropertiesBox(self.top_frame,
                                                                               frame_row=0,
                                                                               frame_col=0,
                                                                               logger=self.log,
                                                                               main_window=self.main_window,
                                                                               canvas_frame = self)
        # Create a trash icon.
        self.trash_icon = trash_icon.TrashIcon(self.bottom_frame,
                                               assigned_row=0,
                                               assigned_col=0,
                                               sticky='sw')

        # Add empty slots.
        for slot_number in range(3):
            self.add_slot()

        self.trigger_configure_event()

    def add_slot(self):
        """
        Add an empty slot. Change the dynamic sizing of the canvas based on which is the last slot.
        :return:
        """
        # Get the new column number based on existing slots
        new_col = len(self.slots) + 3
        # Create the empty layer properties box
        new_layer_box = canvas_properties_box.LayerPropertiesBox(self.scrollable_frame,
                                                                 frame_row=2,
                                                                 frame_col=new_col,
                                                                 logger=self.log,
                                                                 main_window=self.main_window)

        # Change the dynamic sizing of canvas frame grid slots
        self.scrollable_frame.columnconfigure(new_col, weight=0)
        self.scrollable_frame.columnconfigure(new_col+1, weight=1)

        # Add the new slot
        self.slots.append(new_layer_box)
        # Update the slots displayed on the canvas
        self.scrollable_frame.update_idletasks()

    def remove_slot(self):
        """
        Remove a slot from the canvas. Change the dynamic sizing of the canvas grid.
        :return: None
        """
        # Get the slot to be removed.
        slot_number = len(self.slots) + 2
        # Change the dynamic sizing
        self.scrollable_frame.columnconfigure(slot_number, weight=1)
        self.scrollable_frame.columnconfigure(slot_number + 1, weight=0)
        # Remove and destroy the slot
        box = self.slots.pop()
        box.frame.destroy()
        # Update the slots that are displayed by the canvas
        self.scrollable_frame.update_idletasks()

    def get_all_slot_attributes(self):
        """
        Return a dictionary entry containing all layer data.
        :return: None
        """
        slot_info_list = list()
        for slot in self.slots:
            slot_info_list.append(slot.get_attributes())
        layer_information = {'layers':slot_info_list}
        return layer_information

    def get_all_project_properties(self):
        """
        Return all layer and canvas properties in a dictionary.
        :return: None
        """
        # Copy by value. NOT by reference
        props = copy.deepcopy(self.canvas_properties_box.get_properties())

        props.update(self.get_all_slot_attributes())
        return props

    def clear_slots(self):
        """
        Remove all slots from the canvas
        :return: None
        """
        for slot in self.slots:
            slot.clear_slot_attributes()

    def create_new_canvas(self):
        """
        Clear all layer properties boxes from the canvas. Convert to empty layers. Set canvas properties to default.
        :return: None
        """
        old_count = self.canvas_properties_box.box_properties['component_slots']
        self.canvas_properties_box.edit_canvas_attributes(new_canvas_name='new_canvas_{}'.format(1),
                                                          new_slot_count=3,
                                                          new_data_path='None',
                                                          new_project_dir=os.path.join(os.path.expanduser('~'), 'Desktop'),
                                                          new_training_size=.5,
                                                          new_optimizer='sgd',
                                                          new_loss='mean_squared_error',
                                                          new_epochs=1,
                                                          old_count=old_count)
        self.clear_slots()
