# LIBRARIES
import pandas as pd
from mood_funcs import *

# FUNCTIONS
## REFRESH SHEETS TRACKER
def refresh_sheet_tracker(tracker, data):
    for i in range(0, len(data)):
        row = data.applymap(str).iloc[i].values
        print(row)
        tracker.append_row(list(row), value_input_option = 'USER_ENTERED')

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