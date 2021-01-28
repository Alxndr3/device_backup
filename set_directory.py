import shelve
from lib import *


# Set Directory to Save Files.
def set_directory():
    while True:
        draw_header('Set Path For Backup\'')
        device = ['Firewall', 'Switch', 'Quit']
        option = print_menu(device)
        if option == 1 or option == 2:
            directory_path = str(input('Path: '))
            with shelve.open('db_path', 'c', writeback=True) as db_path:
                if len(list(db_path)) < 1:
                    db_path[device[option - 1].lower()] = directory_path
                else:
                    db_path[device[option - 1].lower()] = directory_path
        else:
            break


# List Directories Path.
def list_path():
    with shelve.open('db_path', 'c') as db:
        for k, v in db.items():
            print(k, v)


# Get desired path.
def get_path(device):
    with shelve.open('db_path', 'c') as db:
        return db[device]

