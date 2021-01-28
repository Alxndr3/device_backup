#! /bin/env python3
import getpass
import shelve
import subprocess
from lib import *


# List devices from database.
def db_list():
    subprocess.run(['clear'])
    while True:
        draw_header('List Devices')
        device = ['Firewall', 'Switch', 'Quit']
        option = print_menu(device)
        if option == 1 or option == 2:
            with shelve.open(device[option - 1].lower(), 'c') as device_shelf:
                print(f'{"Hostname --------- ":<12}{"IP --------- ":<13}{"User --------- ":<12}')
                for key, value in list(device_shelf.items()):
                    print(f'{key:<18}{value[0]:<14}{value[1]:<12}')
            print(print_line())
            continue
        else:
            print("Good Bye")
            break


# Insert a new device to database.
def insert_device():
    subprocess.run(['clear'])
    while True:
        draw_header('Insert Device')
        device = ['Firewall', 'Switch', 'Quit']
        option = print_menu(device)
        new_device = list()
        if option == 1 or option == 2:
            hostname = str(input('Hostname: '))
            new_device.append(str(input('IP Address: ')))
            new_device.append(str(input('Username: ')))
            new_device.append(getpass.getpass('Password: '))
            with shelve.open(device[option - 1].lower(), 'c',  writeback=True) as device_shelf:
                if len(list(device_shelf)) < 1:
                    device_shelf[hostname] = new_device
                else:
                    device_shelf[hostname] = new_device
        else:
            print("Good Bye")
            break


# Delete device from database.
def delete_device():
    subprocess.run(['clear'])
    while True:
        draw_header('Delete Device')
        device = ['Firewall', 'Switch', 'Quit']
        option = print_menu(device)
        if option == 1 or option == 2:
            hostname = str(input('Hostname of device to delete: '))
            with shelve.open(device[option - 1].lower(), 'c') as device_shelf:
                del device_shelf[hostname]
        else:
            print("Good Bye")
            break

#db_list()
