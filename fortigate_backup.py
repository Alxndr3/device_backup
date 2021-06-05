#! /usr/bin/env python3
import logging
import os
import paramiko
import set_directory
import shelve
from datetime import date
from scp import SCPClient

#logging.basicConfig(filename=f'./log/{date.today()}_error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def backup_firewall():
    with shelve.open('db_path', 'c') as db:
        try:
            value = db['firewall']
        except KeyError:
            print('Please, define a directory to save configuration files.')
#            set_directory.set_directory()
#            return False

        print("aqui")

    with shelve.open('firewall', 'c') as fw_shelf:
        for key, firewall in fw_shelf.items():
            client = paramiko.client.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            try:
                client.connect(firewall[0], 22, firewall[1], firewall[2])
            except TimeoutError:
                logging.error(f'Time Out Error on {firewall[0]}')
                continue

            except ConnectionError:
                logging.error(f'Connection Error on {firewall[0]}')
                continue

            except paramiko.ssh_exception:
                logging.error(f'Connection Error on {key}')
                continue

            print(f'Backing UP: {key}')

            with SCPClient(client.get_transport()) as scp:
                path = set_directory.get_path('firewall')
                if not os.path.exists(f'{path}/{key}'):
                    os.makedirs(f'{path}/{key}')
                scp.get('sys_config', f'{path}/{key}/{firewall[0]}-{date.today()}.conf')

            print('Done')

# backup_firewall()
