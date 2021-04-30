#! /bin/env python3
import os
import logging
import shelve
import smtplib
from datetime import date
from email.message import EmailMessage

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(level=logging.CRITICAL)


def send_email():
    # print('starting send_email()')
    # os.chdir('/home/alexandre/')
    # print(os.getcwd())
    # Retrieve email address and password from environment variables.
    EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
    EMAIL_PASS = os.environ.get("EMAIL_PASS")

    with shelve.open('db_path', 'c') as db:
        for directory in db.values():
            try:
                os.chdir(directory)
            except FileNotFoundError:
                continue

            for sub_dir in os.listdir():
                logging.debug(sub_dir)
                if os.path.isfile(sub_dir):
                    continue
                if os.path.isdir(sub_dir) and not sub_dir.startswith('.'):
                    logging.debug(sub_dir)
                    os.chdir(sub_dir)
                    logging.debug(os.getcwd())
                    # Using EmailMessage imported from email.message module from email
                    # package to set header fields for the message.
                    msg = EmailMessage()
                    msg['Subject'] = f'Devices Report {str(sub_dir)}'
                    msg['From'] = EMAIL_ADDRESS
                    msg['To'] = EMAIL_ADDRESS
                    msg.set_content('Devices Report')

                    # If report exists in folder assign it to variables to attach it to email message
                    reports = ['difference_report_' + str(date.today()) + '.html', 'full_report_' + str(date.today()) + '.html']
                    for report in reports:
                        if os.path.isfile(report):
                            with open(report, 'rb') as f:
                                attachment = f.read()
                                attachment_name = f.name

                            # Add attachment to email message.
                            msg.add_attachment(attachment, maintype='application', subtype='octet-stream', filename=attachment_name)

                    # Login into email client and send message.
                    if os.path.isfile(report):
                        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                            smtp.login(EMAIL_ADDRESS, EMAIL_PASS)
                            smtp.send_message(msg)
                else:
                    pass
                os.chdir('..')
                logging.debug(os.getcwd())

# send_email()
