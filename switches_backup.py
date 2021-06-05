#!/bin/env python3
import os
import logging
import paramiko
import shelve
import set_directory
from datetime import date
from scp import SCPClient

logging.basicConfig(filename=f'./log/{date.today}_error.log',
        level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


def backup_switches():

    with shelve.open('db_path', 'c') as db:
        try:
            value = db['switch']
            return True
        except KeyError:
            print('Please, define a directory to save configuration files.')
#            set_directory.set_directory()
#            return False

    path = set_directory.get_path('switch')

    with shelve.open('switch', 'c') as sw_shelf:
        for key, switch in sw_shelf.items():
            client = paramiko.client.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                client.connect(switch[0], 22, switch[1], switch[2], look_for_keys=False, allow_agent=False)
            except TimeoutError:
                logging.error(f'Time Out on {key}')
                continue
            except ConnectionError:
                logging.error(f'Connection Error on {key}')
                continue
            except paramiko.ssh_exception:
                logging.error(f'Connection Error on {key}')
                continue
            print(f'Backing up {key}')
            with SCPClient(client.get_transport()) as scp:
                if not os.path.exists(f'{path}/{key}'):
                    os.makedirs(f'{path}/bkp_switches/{key}')
                scp.get('startup.cfg', f'{path}/{key}/{key}-{date.today()}.cfg')
            print('Done')


# backup_switches()
