# LIBRARIES
from datetime import datetime
import win32com.client as win32

from fitbit_funcs import *


# PARAMETERS

FINAL_PATH =  r'C:\Users\Patrick\OneDrive\TRAINING\FITNESS DASHBOARD\Fitness Tracker.xlsx'
SLEEP_PATH = r'C:\Users\Patrick\OneDrive\TRAINING\FITNESS DASHBOARD\fitbit-data\sleep\{}-sleep.csv'.format(DATE_STR)
BAF_PATH = r'C:\Users\Patrick\OneDrive\TRAINING\FITNESS DASHBOARD\fitbit-data\body\{}-body.csv'.format(DATE_STR)

