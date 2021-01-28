import shelve
from time import sleep
w = 158


def print_line(size=w):
    print('-' * w)


def draw_header(text):
    print_line()
    print(text.center(w))
    print_line()


def choose_option(message):
    while True:
        try:
            option = int(input(message))
            return option
        except (ValueError, TypeError):
            print('\033[35mPlease, insert a valid option.\033[m')
            continue
        except KeyboardInterrupt:
            print('\n\033[31mBye;\033[m')
            return 0
        else:
            return option


def print_menu(menu_list):
    count = 1
    for item in menu_list:
        print(f'{count} - {item}')
        count += 1
    print_line()
    option = choose_option("> ")
    return option


def open_path():
    with shelve.open('path_db') as path_db:
        return path_db

