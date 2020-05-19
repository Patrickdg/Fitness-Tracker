# LIBRARIES
from data_funcs import * 

# MAIN 
def main(trackers, days):
    sheets = map(str.lower, trackers)

    for tracker, sheet in zip(trackers, sheets): 
        for day in days: 
            data = extract_data(sheet, [day])
            if not data.empty: 
                refresh_sheet_tracker(tracker, data)
                print(f"{sheet} data updated for {day}.")

if __name__ == "__main__":
    testing = True
    trackers = [BAF, SLEEP, EMOODS]

    if testing: 
        date_range = ['2020-05-01', '2020-05-02']
    else:
        date_range = set_date_range(BAF)

    main(trackers, date_range)

