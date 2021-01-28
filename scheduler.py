#!/usr/bin/env python3
import os
import shelve
import re
import subprocess
import time
from lib import draw_header


def schedule_job():
    draw_header(f'Now it is: {time.strftime("%H:%M:%S")}')
    # Regular expressiton to text if the user input for hour is in the correct
    # format.
    hour_regex = re.compile(r'[0-2]\d:[0-5]\d')
    hour = str(input("Time to run job [hh:mm]: "))
    mo = hour_regex.search(hour)
    if mo:
        with shelve.open("time_to_run", 'c') as time_db:
            time_db['clock'] = hour
    else:
        print('\nIt\'s supposed to be a 24h time format, eg. 09:59.\n')

def show_time():
    with shelve.open("time_to_run", 'c') as tr:
        draw_header(f'The job will run at {tr.get("clock")}')


def run_schedule_service():
    subprocess.run(['nohup python3 -u run.py > error.txt 2>&1 &'], shell=True)
    # subprocess.run(['nohup python3 -u run.py > /dev/null 2>&1 &'], shell=True)

# show_time()
# schedule_job()
# run_schedule_service()
