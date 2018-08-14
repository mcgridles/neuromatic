import tkinter


class GenericButton(object):

    def __init__(self,
                 root,
                 button_label,
                 passed_function,
                 assigned_row=0,
                 assigned_col=0,
                 sticky='nsew',
                 logger=None,
                 main_window=None):
        """
        Parent class to the drag and drop buttons. Contains functionality to assign a function to the button and assign
        the widget position.
        :param root: Tkinter.Widget - The Tkinter parent widget in which this class is encapsulated.
        :param button_label: str - The string displayed on the button.
        :param passed_function: function - The function executed on the button click.
        :param assigned_row: int - The row on which the button will exist on root.
        :param assigned_col: int - The column on which the button will exist on root.
        :param sticky: str - The sides of root to which the widget will adhere and expand.
        :param logger: funciton - The function to which status strings can be passed.
        :param main_window: Tkinter.Tk - The main window of the application. Used to manage application data.
        """
        self.root = root
        self.passed_function = passed_function
        self.b = tkinter.Button(self.root, text=button_label, command=self.button_callback)
        self.b.grid(row=assigned_row, column=assigned_col, sticky=sticky)
        self.log = logger
        self.main_window = main_window

    def button_callback(self):
        """
        Run the function passed by through the constructor.
        :return: None
        """
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
        """
        The LayerButton adds the drag and drop methods to the GenericButton.
        :param root: Tkinter.Widget - The Tkinter parent widget in which this class is encapsulated.
        :param button_label: str - The string displayed on the button.
        :param passed_function: function - The function executed on the button click.
        :param assigned_row: int - The row on which the button will exist on root.
        :param assigned_col: int - The column on which the button will exist on root.
        :param sticky: str - The sides of root to which the widget will adhere and expand.
        :param logger: funciton - The function to which status strings can be passed.
        :param main_window: Tkinter.Tk - The main window of the application. Used to manage application data.
        """

        super(LayerButton, self).__init__(root=root,
                                          button_label=button_label,
                                          passed_function=passed_function,
                                          assigned_row=assigned_row,
                                          assigned_col=assigned_col,
                                          sticky=sticky,
                                          logger=logger,
                                          main_window=main_window)

        # Track the button's layer type
        self.layer_type = layer_type
        # The layer buttons are made draggable for canvas design.
        self.make_draggable()

    def make_draggable(self):
        """
        Bind events to the button so that the drag and drop methods will be called.
        :return: None
        """
        # A single click will signify the start of drag and drop
        self.b.bind('<Button-1>', self.on_start)
        self.b.bind('<B1-Motion>', self.on_drag)
        # Releasing the click will end drag and drop
        self.b.bind('<ButtonRelease-1>', self.on_drop)
        # Change the cursor while positioned over the widget
        self.b.configure(cursor='hand2')

    def on_start(self, event):
        """
        Store the layer type in the main window so that a different widget, that is part of the main window, can
        inherit the layer type on drop.
        :param event: Tkinter.target - A Tkinter variable that represents a user's interaction with the GUI.
        :return: None
        """
        self.main_window.current_layer_type = self.layer_type

    def on_drag(self, event):
        """
        Change the cursor to signify the drag event.
        :param event: Tkinter.target - A Tkinter variable that represents a user's interaction with the GUI.
        :return: None
        """
        self.b.configure(cursor='middlebutton')

    def on_drop(self, event):
        """
        Check the cursor's position at the end of a drag and drop. This will return the target widget at that position
        and trigger a Tkinter event which will run a method of that widget class.
        :param event: Tkinter.target - A Tkinter variable that represents a user's interaction with the GUI.
        :return: None
        """
        self.b.configure(cursor='hand2')
        # Get the location of the cursor
        x, y = self.root.winfo_pointerx(), self.root.winfo_pointery()
        # Get the widget at that location
        target = event.widget.winfo_containing(x, y)
        try:
            # Generate the <<Inherit>> event that could trigger a method in the target widget
            target.event_generate('<<Inherit>>', when='tail')
        except:
            pass
