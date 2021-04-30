import os
import difflib
import shelve
import logging
from filecmp import cmp
from datetime import date
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
#logging.disable(logging.CRITICAL)


# Generate full report showing full configuration file and its changes.
def generate_full_report(file_1, file_2):
    # os.chdir(report_dir)
    with open(file_1, 'r') as f1:
        f1 = f1.readlines()
    with open(file_2, 'r') as f2:
        f2 = f2.readlines()
    difference = difflib.HtmlDiff().make_file(f2, f1)
    with open('full_report.html', 'w') as full_report:
        full_report.write(difference)


# Generate report containing only changes occurred in the configuration file.
def generate_diff_report():  # report_dir):
    #    os.chdir(report_dir)
    with open('full_report.html', 'r') as full_report:
        # Make a soup object for each line of full_report.html.
        for line in full_report:
            report_soup = BeautifulSoup(line, features='html.parser')
            anchor = report_soup.find(class_="diff_next")
            # Exclude lines which didn't suffered changes.
            if anchor is None or anchor.text == 'f' or anchor.text == 'n' or anchor.text == 't':
                with open('difference_report.html', 'a') as difference_report:
                    difference_report.write(line)


# Access each folder of each device and run report generator
def run_report():
    with shelve.open('db_path') as db:
        for path in db.values():
            try:
                os.chdir(path)
            except FileNotFoundError:
                continue

            for directory in os.listdir():
                logging.error(directory)
                if not os.path.isdir(directory) or directory.startswith('.'):
                    pass
                else:
                    os.chdir(directory)
                    # The next four lines are for removing .html files of being
                    # processed by de report functions
                    dir_files = os.listdir()
                    # print(os.getcwd())
                    for file_ in dir_files:
                        if file_.endswith('.html'):
                            dir_files.remove(file_)
                        logging.debug(dir_files)
                    logging.debug(os.getcwd())
                    dir_files.sort()
                    file_1 = dir_files[-1]
                    file_2 = dir_files[-2]
                    logging.debug(file_1)
                    logging.debug(file_2)
                    if cmp(file_1, file_2, shallow=True) is False:
                        generate_full_report(file_1, file_2)
                        generate_diff_report()
                        os.rename('full_report.html', 'full_report_' + str(date.today()) + '.html')
                        os.rename('difference_report.html', 'difference_report_' + str(date.today()) + '.html')
                    os.chdir('..')

# run_report()

