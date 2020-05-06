# LIBRARIES
import os
from datetime import datetime
import win32com.client as win32
import json
import time
import imp

import fitbit
from fitbit import gather_keys_oauth2 as Oauth2

import fitbit_data as fb
imp.reload(fb)

# PARAMETERS
FILE_DATE = datetime.today()
DATE_STR = FILE_DATE.strftime('%m-%d-%Y')

FINAL_PATH =  r'C:\Users\Patrick\OneDrive\TRAINING\FITNESS DASHBOARD\Fitness Tracker.xlsx'
SLEEP_PATH = r'C:\Users\Patrick\OneDrive\TRAINING\FITNESS DASHBOARD\fitbit-data\sleep\{}-sleep.csv'.format(DATE_STR)
BAF_PATH = r'C:\Users\Patrick\OneDrive\TRAINING\FITNESS DASHBOARD\fitbit-data\body\{}-body.csv'.format(DATE_STR)

# SETUP
CLIENT_ID = os.environ.get('FB_ID')
CLIENT_SECRET = os.environ.get('FB_SCRET')
KEY = os.environ.get('FB_KEY') # GS
with open(KEY) as key_file:
    KEY = json.load(key_file)

server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
time.sleep(10)

ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])

auth2_client = fitbit.Fitbit(CLIENT_ID, 
                            CLIENT_SECRET, 
                            oath2 = True, 
                            access_token = ACCESS_TOKEN,
                            refresh_token = REFRESH_TOKEN)





