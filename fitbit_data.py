# LIBRARIES
from datetime import datetime
import win32com.client as win32

import fitbit_funcs as fb

import imp
imp.reload(fb)

# PARAMETERS
FILE_DATE = datetime.today()
DATE_STR = FILE_DATE.strftime('%Y-%m-%d')

FINAL_PATH =  r'C:\Users\Patrick\OneDrive\TRAINING\FITNESS DASHBOARD\Fitness Tracker.xlsx'
SLEEP_PATH = r'C:\Users\Patrick\OneDrive\TRAINING\FITNESS DASHBOARD\fitbit-data\sleep\{}-sleep.csv'.format(DATE_STR)
BAF_PATH = r'C:\Users\Patrick\OneDrive\TRAINING\FITNESS DASHBOARD\fitbit-data\body\{}-body.csv'.format(DATE_STR)

