#!/usr/bin/env python3
import subprocess
import db_create
import scheduler
import set_directory
import fortigate_backup
import switches_backup
import send_email
import generate_report
from lib import *

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
        db_create.insert_device()

    elif opt == 2:
        db_create.delete_device()

    elif opt == 3:
        db_create.db_list()

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
                set_directory.set_directory()
            elif path_menu == 2:
                draw_header(f'\n{set_directory.get_path("firewall")}\n{set_directory.get_path("switch")}')
            else:
                break

    elif opt == 6:
        subprocess.run(['clear'])
        while True:
            run_job = print_menu(['Backup Firewall', 'Backup Switches', 'Generate Report', 'Send Report', 'All', 'Quit'])
            if run_job == 1:
                print('Please, Hang On')
                fortigate_backup.backup_firewall()
            elif run_job == 2:
                print('Please, Hang On')
                switches_backup.backup_switches
            elif run_job == 3:
                print('Please, Hang On')
                run_report()
            elif run_job == 4:
                print('Please, Hang On')
                send_email.send_email()
            elif run_job == 5:
                print('Please, Hang On')
                fortigate_backup.backup_firewall()
                switches_backup.backup_switches()
                generate_report.run_report()
                send_email.send_email()
            else:
                break

    else:
        print('Bye')
        break
