# LIBRARIES
from fitbit_funcs import *

# PARAMETERS
TRACKERS = {[SLEEP, BAF, MOODS],
            ['sleep','baf','emoods']}

# MAIN
def main():
    date_range = set_date_range(BAF)

    for tracker, sheet in zip(TRACKERS[0], TRACKERS[1]):
        for day in date_range: 
            data = extract_data(sheet, [day])
            if not data.empty:
                refresh_sheet_tracker(tracker, data)
