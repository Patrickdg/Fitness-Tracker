# LIBRARIES
import os 
import json
import pandas as pd
from datetime import datetime, timedelta
import zipfile

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import fitbit
from fitbit import gather_keys_oauth2 as Oauth2

# SETUP
TODAY = datetime.today()
emoods_path = r'C:\Users\Patrick\OneDrive\TRAINING\FITNESS_DASHBOARD\emoods-data'

##SHEETS
KEY = os.environ.get('GS_KEY')

CLIENT_ID = os.environ.get('FB_ID')
CLIENT_SECRET = os.environ.get('FB_SCRET')

SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
CREDS = ServiceAccountCredentials.from_json_keyfile_name(KEY, SCOPE)
CLIENT = gspread.authorize(CREDS)

BAF = CLIENT.open('Fitness Tracker').worksheet('body_activity_food')
SLEEP = CLIENT.open('Fitness Tracker').worksheet('sleep')
MOODS = CLIENT.open('Fitness Tracker').worksheet('emoods')

##FITBIT
SERVER = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
SERVER.browser_authorize()  
ACCESS_TOKEN = str(SERVER.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(SERVER.fitbit.client.session.token['refresh_token'])

AUTH2_CLIENT = fitbit.Fitbit(CLIENT_ID, 
                            CLIENT_SECRET, 
                            oath2 = True, 
                            access_token = ACCESS_TOKEN,
                            refresh_token = REFRESH_TOKEN)

# FUNCTIONS
def set_date_range(sheet):
    days = []

    last_date = max(sheet.col_values(1)[1:])
    last_date = datetime.strptime(last_date, "%Y-%m-%d")

    num_days = (TODAY - last_date).days
    for day in range(1, num_days): 
        days.append((last_date + timedelta(days = day)).strftime("%Y-%m-%d"))

    return days

def get_sleep_data(sleep_days):
    sleep_data = pd.DataFrame()
    for day in sleep_days:
        sleep_full = AUTH2_CLIENT.sleep(date = day)
        num_sleep_records = sleep_full['summary']['totalSleepRecords']
        # If no sleep entry, then append empty line with date
        # If # sleep entries > 1, Extract MainSleep using n = 1
        if num_sleep_records == 0:
            pass
        else:
            main_sleep = 0 
            if num_sleep_records > 1:
                while main_sleep == 0:
                    for n in range(0,num_sleep_records):
                        if sleep_full['sleep'][n]['isMainSleep'] == True:
                            main_sleep += n
                            break
                        else: 
                            pass
            
            sleep_sleep = sleep_full['sleep'][main_sleep]
            sleep_summary = sleep_full['summary']

            try:
                sleep_df = pd.DataFrame({
                    'date':day,
                    'dateOfSleep':sleep_sleep['dateOfSleep'],
                    'startTime':sleep_sleep['startTime'],
                    'endTime':sleep_sleep['endTime'],
                    'isMainSleep':sleep_sleep['isMainSleep'],
                    'duration':sleep_sleep['duration'],
                    'efficiency':sleep_sleep['efficiency'],
                    'timeInBed':sleep_sleep['timeInBed'],
                    'totalTimeInBed':sleep_summary['totalTimeInBed'],
                    'minutesToFallAsleep':sleep_sleep['minutesToFallAsleep'],
                    'totalMinutesAsleep':sleep_summary['totalMinutesAsleep'],
                    'minutesAsleep':sleep_sleep['minutesAsleep'],
                    'deep':sleep_summary['stages']['deep'],
                    'light':sleep_summary['stages']['light'],
                    'rem':sleep_summary['stages']['rem'],
                    'wake':sleep_summary['stages']['wake'],
                    'minutesAwake':sleep_sleep['minutesAwake'],
                    'minutesAfterWakeup':sleep_sleep['minutesAfterWakeup'],
                    'restlessDuration':sleep_sleep['restlessDuration'],
                    'restlessCount':sleep_sleep['restlessCount'],
                    'awakeDuration':sleep_sleep['awakeDuration'],
                    'awakeCount':sleep_sleep['awakeCount'],
                    'awakeningsCount':sleep_sleep['awakeningsCount']
                    }, index = [0])
                sleep_data = sleep_data.append(sleep_df)
            except KeyError as key: 
                print(f"Key Error: Couldn't find {key}")
 
    return sleep_data

def get_body_data(body_days):
    body_data = pd.DataFrame()
    for day in body_days: 
        body_full = AUTH2_CLIENT.body(date = day)
        if body_full['body']['weight'] == 0: # weight not recorded for the day
            pass 
        else:
            try: 
                body_df = pd.DataFrame({
                    'date':day,
                    'weight':body_full['body']['weight'],
                    'body_fat':body_full['body']['fat'],
                    'bmi': body_full['body']['bmi']
                    }, index = [0])
                body_data = body_data.append(body_df)
            except KeyError as key: 
                print(f"Key Error: Couldn't find {key}")
                
    
    return body_data

def get_activity_data(body_days):
    activity_data = pd.DataFrame()
    for day in body_days: 
        activity_full = AUTH2_CLIENT.activities(date = day)['summary']
        if activity_full['steps'] < 500: # didn't wear watch that day, not enough data 
            pass 
        else:
            try: 
                activity_df = pd.DataFrame({
                    'date':day,
                    'activityCalories':activity_full['activityCalories'],
                    'caloriesBMR':activity_full['caloriesBMR'],
                    'caloriesOut':activity_full['caloriesOut'],
                    'marginalCalories':activity_full['marginalCalories'],
                    'steps':activity_full['steps'],
                    'sedentaryMinutes':activity_full['sedentaryMinutes'],
                    'lightlyActiveMinutes':activity_full['lightlyActiveMinutes'],
                    'fairlyActiveMinutes':activity_full['fairlyActiveMinutes'],
                    'veryActiveMinutes':activity_full['veryActiveMinutes'],
                    'restingHeartRate':activity_full['restingHeartRate'],
                    'hr_OOR_mins':activity_full['heartRateZones'][0]['minutes'],
                    'hr_fatburn_mins':activity_full['heartRateZones'][1]['minutes'],
                    'hr_cardio_mins':activity_full['heartRateZones'][2]['minutes'],
                    'hr_peak_mins':activity_full['heartRateZones'][3]['minutes'],
                }, index = [0]) 
                activity_data = activity_data.append(activity_df)
            except KeyError as key:
                print(f"Key Error: Couldn't find {key}")
    
    return activity_data

def get_food_data(body_days):
    food_data = pd.DataFrame()
    for day in body_days: 
        food_full = AUTH2_CLIENT.foods_log(date = day)['summary']
        if food_full['calories'] == 0: # Cals not recorded for the day
            pass 
        else:
            try: 
                food_df = pd.DataFrame({
                    'date':day,
                    'calories':food_full['calories'],
                    'carbs':food_full['carbs'],
                    'fat':food_full['fat'], 
                    'fiber':food_full['fiber'],
                    'protein':food_full['protein'],
                    'sodium':food_full['sodium'],
                    }, index = [0])
                food_data = food_data.append(food_df)
            except KeyError as key:
                print(f"Key Error: Couldn't find {key}")

    return food_data

def extract_data(sheet, date_range):
    df = pd.DataFrame({'date': date_range})

    if sheet == 'sleep':
        df = get_sleep_data(date_range)
    elif sheet == 'baf': 
        body = get_body_data(date_range)
        activity = get_activity_data(date_range)
        food = get_food_data(date_range)
    
        for set in [body, activity, food]:
            if set.empty: 
                pass
            else: 
                df = pd.merge(df, set,
                                on = 'date', 
                                how = 'outer')
    elif sheet == 'emoods':
        df = get_emoods_data(emoods_path)

    return df

def format_emoods_data(moods_path):
    if os.path.exists(emoods_path + '\export.emoods'):
        os.rename(emoods_path + r'\export.emoods', emoods_path + r'\export.zip')
        with zipfile.ZipFile(emoods_path+r'\export.zip', 'r') as zip_ref:
            zip_ref.extractall(emoods_path)
        
        for file in os.listdir(emoods_path):
            if file != 'entry.csv':
                os.remove(emoods_path+r'\{}'.format(file))

def get_emoods_data(moods_path):
    format_emoods_data(moods_path)
    moods_data = pd.read_csv(moods_path + '\entry.csv')

    old_entries = moods_data.iloc[:,1].isin(MOODS.col_values(1)[1:])
    moods_data = moods_data[~old_entries].iloc[:,1:7]

    return moods_data

# OTHER FUNCS
## REFRESH SHEETS TRACKER
def refresh_sheet_tracker(tracker, data):
    for i in range(0, len(data)):
        row = data.applymap(str).iloc[i].values
        print(row)
        tracker.append_row(list(row), value_input_option = 'USER_ENTERED')

# TESTING 
if __name__ == "__main__":
    testing = True
    if testing: 
        date_range = ['2020-05-01', '2020-05-02']
    else:
        date_range = set_date_range(BAF)

    for tracker, sheet in zip([SLEEP, BAF, MOODS], ['sleep','baf', 'emoods']):
        for day in date_range: 
            data = extract_data(sheet, [day])
            if not data.empty:
                refresh_sheet_tracker(tracker, data)
