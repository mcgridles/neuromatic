import tkinter
import os
from tkinter import filedialog

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
USER_HOME = os.path.expanduser('~')

VALID_TYPES = {
    'all': ('all files', '*'),
    'csv': ('csv', '*.csv'),
    'python': ('Python', '*.py'),
    'h5py': ('h5py', '*.h5py')
}


def user_get_file(init_dir, file_type_list, title):
    if type(file_type_list) is not list or tuple:
        file_type_list = [file_type_list]

    file_types = list()

    for file_type in file_type_list:
        assert file_type in VALID_TYPES, '{} is not valid file type.'.format(file_type)
        file_types.append(VALID_TYPES[file_type])

    assert os.path.isdir(init_dir), '{} is not a valid directory.'.format(init_dir)

    file_name = tkinter.filedialog.askopenfilename(initialdir=init_dir,
                                                   title=title,
                                                   filetypes=file_types)

    return file_name


def user_get_directory(title, init_dir):
    assert os.path.isdir(init_dir), '{} is not a valid directory.'.format(init_dir)

    dir_name = tkinter.filedialog.askdirectory(title=title, initialdir=init_dir)

    return dir_name


def test_utils():
    print(user_get_file(USER_HOME, 'all', 'test'))
    print(user_get_directory('test', USER_HOME))


if __name__ == "__main__":
    test_utils()
