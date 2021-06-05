#! /bin/env python3
import getpass
import re
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
                subprocess.run(['clear'])
                print(f'{"Hostname --------- ":<12}{"IP --------- ":<13}{"User --------- ":<12}')
                for key, value in list(device_shelf.items()):
                    print(f'{key:<18}{value[0]:<14}{value[1]:<12}')
                print_line()

            continue
        else:
            print("Good Bye")
            break


# Insert a new device to database.
def insert_device():
    # Regular expression to validate IPv4.
    ip_address_regex = re.compile(r'^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.'
                                    '(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.'
                                    '(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.'
                                    '(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$')

    subprocess.run(['clear'])

    while True:
        draw_header('Insert Device')
        device = ['Firewall', 'Switch', 'Quit']
        option = print_menu(device)
        new_device = list()
        if option == 1 or option == 2:
            hostname = str(input('Hostname: '))
            device_ip_addr = str(input('IP Address: '))
            device_match_obj = ip_address_regex.search(device_ip_addr)
            # If inserted IP address is valid shelve object is created
            if device_match_obj:
                new_device.append(device_match_obj.group())
                new_device.append(str(input('Username: ')))
                new_device.append(getpass.getpass('Password: '))
                with shelve.open(device[option - 1].lower(), 'c',  writeback=True) as device_shelf:
                    if len(list(device_shelf)) < 1:
                        device_shelf[hostname] = new_device
                    else:
                        device_shelf[hostname] = new_device
            else:
                print('\nNot a valid IP address.\n')
        else:
            print("Good Bye")
            break
        print('\n' + '\033[93m' + 'New device ready' + '\033[0m' + '\n')


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

# db_list()
# insert_device()
# delete_device()

