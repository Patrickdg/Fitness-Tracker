# LIBRARIES
import pandas as pd

# GET DATA
def get_sleep_data(sleep_days):
    sleep_data = pd.DataFrame()

    for day in sleep_days:
        sleep_full = auth2_client.sleep(date = day)

        num_sleep_records = sleep_full['summary']['totalSleepRecords']

        # If no sleep entry, then append empty line with date
        # If # sleep entries > 1, Extract MainSleep using n = 1
        if num_sleep_records == 0:
            pass
        else:
            if num_sleep_records == 1:
                main_sleep = 0
            elif num_sleep_records > 1:
                main_sleep = 0
                while main_sleep == 0:
                    for n in range(0,num_sleep_records):
                        if sleep_full['sleep'][n]['isMainSleep'] == True:
                            main_sleep += n
                            break
                        else: 
                            pass
            
            sleep_sleep = sleep_full['sleep'][main_sleep]
            sleep_summary = sleep_full['summary']

            sleep_df = pd.DataFrame({
                'date':day,
                'awakeCount':sleep_sleep['awakeCount'],
                'awakeDuration':sleep_sleep['awakeDuration'],
                'awakeningsCount':sleep_sleep['awakeningsCount'],
                'duration':sleep_sleep['duration'],
                'efficiency':sleep_sleep['efficiency'],
                'endTime':sleep_sleep['endTime'],
                'isMainSleep':sleep_sleep['isMainSleep'],
                'minutesAfterWakeup':sleep_sleep['minutesAfterWakeup'],
                'minutesAsleep':sleep_sleep['minutesAsleep'],
                'minutesAwake':sleep_sleep['minutesAwake'],
                'minutesToFallAsleep':sleep_sleep['minutesToFallAsleep'],
                'restlessCount':sleep_sleep['restlessCount'],
                'restlessDuration':sleep_sleep['restlessDuration'],
                'startTime':sleep_sleep['startTime'],
                'timeInBed':sleep_sleep['timeInBed'],

                'deep':sleep_summary['stages']['deep'],
                'light':sleep_summary['stages']['light'],
                'rem':sleep_summary['stages']['rem'],
                'wake':sleep_summary['stages']['wake'],
                'totalMinutesAsleep':sleep_summary['totalMinutesAsleep'],
                'totalSleepRecords':sleep_summary['totalSleepRecords'],
                'totalTimeInBed':sleep_summary['totalTimeInBed']
            }, index = [0])
                
            sleep_data = sleep_data.append(sleep_df)
 
    return sleep_data

def get_body_data(body_days):
    body_data = pd.DataFrame()

    for day in body_days: 
        body_full = auth2_client.body(date = day)

        if body_full['body']['weight'] == 0:
            pass 
        else:
            body_df = pd.DataFrame({
                'date':day,
                'weight':body_full['body']['weight'],
                'body_fat':body_full['body']['fat'],
                'bmi': body_full['body']['bmi']
            }, index = [0])

            body_data = body_data.append(body_df)
    
    return body_data

def get_activity_data(body_days):
    activity_data = pd.DataFrame()

    for day in body_days: 
        activity_full = auth2_client.activities(date = day)['summary']

        if activity_full['steps'] < 500:
            pass 
        else:
            activity_df = pd.DataFrame({
                'date':day,
                'activeScore':activity_full['activeScore'],
                'activityCalories':activity_full['activityCalories'],
                'caloriesBMR':activity_full['caloriesBMR'],
                'caloriesOut':activity_full['caloriesOut'],
                'marginalCalories':activity_full['marginalCalories'],
                'steps':activity_full['steps'],
                'sedentaryMinutes':activity_full['sedentaryMinutes'],
                'lightlyActiveMinutes':activity_full['lightlyActiveMinutes'],
                'fairlyActiveMinutes':activity_full['fairlyActiveMinutes'],
                'veryActiveMinutes':activity_full['veryActiveMinutes'],
                #'restingHeartRate':activity_full['restingHeartRate'],
                'hr_OOR_mins':activity_full['heartRateZones'][0]['minutes'],
                'hr_fatburn_mins':activity_full['heartRateZones'][1]['minutes'],
                'hr_cardio_mins':activity_full['heartRateZones'][2]['minutes'],
                'hr_peak_mins':activity_full['heartRateZones'][3]['minutes'],
            }, index = [0])

            activity_data = activity_data.append(activity_df)
    
    return activity_data

def get_food_data(body_days):
    food_data = pd.DataFrame()

    for day in body_days: 
        food_full = auth2_client.foods_log(date = day)['summary']

        if food_full['calories'] == 0:
            pass 
        else:
            food_df = pd.DataFrame({
                'date':day,
                'calories':food_full['calories'],
                'carbs':food_full['carbs'],
                'fat':food_full['fat'], 
                'fiber':food_full['fiber'],
                'protein':food_full['protein'],
                'sodium':food_full['sodium'],
                'water':food_full['water']
            }, index = [0])

            food_data = food_data.append(food_df)
    
    return food_data

def extract_and_merge_data():
    # Sleep data
    sleep_days = set_date_range('Fitbit - Sleep')

    sleep = get_sleep_data(sleep_days)
    sleep = pd.merge(pd.DataFrame({'date':sleep_days}), sleep, 
                    on = 'date',
                    how = 'outer')

    # Body, Activity, Sleep data
    body_days = set_date_range('Fitbit - Body')

    body = get_body_data(body_days)
    activity = get_activity_data(body_days)
    food = get_food_data(body_days)

    
    if body.empty: 
        pass
    else:
        body_activity_food = pd.merge(pd.DataFrame({'date':body_days}), body,
                        on = 'date',
                        how = 'outer')

    if activity.empty:
        pass
    else:
        body_activity_food = pd.merge(body, activity, 
                        on = 'date',
                        how = 'outer')

    if food.empty:
        pass
    else:
        body_activity_food = pd.merge(body_activity_food, food, 
                        on = 'date',
                        how = 'outer')

    return sleep, body_activity_food


# OTHER FUNCS
## REFRESH SHEETS TRACKER
def refresh_excel_tracker():
    Xlsx = win32.DispatchEx('Excel.Application')
    Xlsx.DisplayAlerts = False
    Xlsx.Visible = True
    Xlsx = Xlsx.Workbooks.Open(file_path)
    time.sleep(10)
    
    Xlsx.RefreshAll()
    time.sleep(10)

    Xlsx.Save()