import os
import tkinter as tk


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class TrashIcon(object):

    def __init__(self,
                 root,
                 assigned_row=0,
                 assigned_col=0,
                 sticky='nsew'):
        """
        This icon is used to trigger the remove layer process.
        :param root: tkinter.Widget - Parent widget which encapsulates the icon.
        :param assigned_row: int - Row on which the icon will exist on the parent widget.
        :param assigned_col: int - Column on which the icon will exist on the parent widget.
        :param sticky: str - sides to which the icon will adhere
        """

        image_path = os.path.join(CURRENT_DIR, 'trash-3.gif')
        self.icon_photo = tk.PhotoImage(file=image_path)

        self.trash_icon = tk.Label(root, image=self.icon_photo)
        self.trash_icon.image = self.icon_photo
        self.trash_icon.grid(row=assigned_row, column=assigned_col, sticky=sticky)
