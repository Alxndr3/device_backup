import schedule
import shelve
import time
import send_email
from datetime import datetime, timedelta
from fortigate_backup import backup_firewall
from generate_report import run_report
from switches_backup import backup_switches
from scheduler import schedule_job


def get_time():
    with shelve.open('time_to_run') as tr:
        time_str_1 = tr.get('clock')
        time_obj_1 = datetime.strptime(time_str_1, "%H:%M")
        time_obj_2 = time_obj_1 + timedelta(minutes=3)
        time_str_2 = str(time_obj_2.hour).zfill(2) + ':' + str(time_obj_2.minute).zfill(2)
        return time_str_1, time_str_2

# schedule_job()
run_time_1 = get_time()[0]
run_time_2 = get_time()[1]
# print(run_time_1, run_time_2)
#
schedule.every().day.at(run_time_1).do(backup_firewall)
schedule.every().day.at(run_time_1).do(backup_switches)
schedule.every().day.at(run_time_1).do(run_report)
schedule.every().day.at(run_time_1).do(send_email.send_email)

while True:
    schedule.run_pending()
    time.sleep(1)
