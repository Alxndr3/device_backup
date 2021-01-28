#! /bin/env python3
from db_create import *
from lib import *
from generate_report import run_report
from fortigate_backup import backup_firewall
from set_directory import set_directory
from set_directory import get_path
from send_email import send_email
from switches_backup import backup_switches
import subprocess
import shelve
import scheduler


while True:
    subprocess.run(['clear'])
    draw_header('NETWORK DEVICES SETTINGS CONTROL')
    opt = print_menu(['Add Device',
                      'Delete Device',
                      'List Devices',
                      'Schedule Job',
                      'Save to',
                      'Run Now',
                      'Quit'])
    if opt == 1:
        insert_device()

    elif opt == 2:
        delete_device()

    elif opt == 3:
        db_list()

    elif opt == 4:
        subprocess.run(['clear'])
        while True:
            sch_opt = print_menu(['Schedule Job', 'Show Time Scheduled', 'Quit'])
            if sch_opt == 1:
                subprocess.run(['clear'])
                scheduler.schedule_job()
                scheduler.run_schedule_service()

                continue
            elif sch_opt == 2:
                subprocess.run(['clear'])
                scheduler.show_time()
                continue
            else:
                break

    elif opt == 5:
        subprocess.run(['clear'])
        while True:
            path_menu = print_menu(['Set Path', 'Get Path', 'Quit'])
            if path_menu == 1:
                set_directory()
            elif path_menu == 2:
                draw_header(f'\n{get_path("firewall")}\n{get_path("switch")}')
            else:
                break

    elif opt == 6:
        subprocess.run(['clear'])
        while True:
            run_job = print_menu(['Backup Firewall', 'Backup Switches', 'Generate Report', 'Send Report', 'All', 'Quit'])
            if run_job == 1:
                print('Please, Hang On')
                backup_firewall()
            elif run_job == 2:
                print('Please, Hang On')
                backup_switches()
            elif run_job == 3:
                print('Please, Hang On')
                run_report()
            elif run_job == 4:
                print('Please, Hang On')
                send_email()
            elif run_job == 5:
                print('Please, Hang On')
                backup_firewall()
                backup_switches()
                run_report()
                send_email()
            else:
                break

    else:
        print('Bye')
        break

