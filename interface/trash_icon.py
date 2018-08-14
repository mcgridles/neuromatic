import os
import tkinter as tk


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class TrashIcon(object):

    def __init__(self,
                 root,
                 command,
                 frame_row=0,
                 frame_col=0,
                 sticky='nsew'):

        image_path = os.path.join(CURRENT_DIR, 'trash-3.gif')
        self.icon_photo = tk.PhotoImage(file=image_path)

        self.trash_icon = tk.Label(root, image=self.icon_photo)
        self.trash_icon.image = self.icon_photo
        self.trash_icon.grid(row=frame_row, column=frame_col, sticky=sticky)
        self.trash_icon.bind('<Double-Button-1>', command)
