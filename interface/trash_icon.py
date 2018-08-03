import os
import tkinter as tk


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def callback(event):
    # print('here')
    print("clicked at", event.x, event.y)


class TrashIcon(object):

    def __init__(self,
                 root,
                 command,
                 frame_row=0,
                 frame_col=0,
                 sticky='nsew'):

        image_path = os.path.join(CURRENT_DIR, 'trash-3.gif')
        self.icon_photo = tk.PhotoImage(file=image_path)
        # self.trash_icon = tk.Button(root,
        #                             height=40,
        #                             width=40,
        #                             image=self.icon_photo,
        #                             command=command)

        self.trash_icon = tk.Label(root, image=self.icon_photo)
        self.trash_icon.image = self.icon_photo
        self.trash_icon.grid(row=frame_row, column=frame_col, sticky=sticky)
        self.trash_icon.bind('<Double-Button-1>', command)


        # self.trash_icon.bind('<ButtonRelease-1>', command)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('TrashIcon Test')
    root.geometry('400x400')

    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    icon_frame = tk.Frame(root, bg='green', height=200, width=200, pady=3, padx=3)
    icon_frame.grid(row=0, column=0, sticky='nsew')

    blank_frame_1 = tk.Frame(root, bg='blue', height=200, width=200, pady=3, padx=3)
    blank_frame_1.grid(row=0, column=1, sticky='nsew')

    blank_frame_2 = tk.Frame(root, bg='cyan', height=200, width=200, pady=3, padx=3)
    blank_frame_2.grid(row=1, column=0, sticky='nsew')

    blank_frame_3 = tk.Frame(root, bg='yellow', height=200, width=200, pady=3, padx=3)
    blank_frame_3.grid(row=1, column=1, sticky='nsew')

    TrashIcon(icon_frame, callback)

    root.mainloop()