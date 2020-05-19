# LIBRARIES
import fitbit_funcs
import imp
imp.reload(fitbit_funcs)

# MAIN 
def main(trackers, sheets, days):
    for tracker, sheet in zip(trackers, sheets): 
        for day in days: 
            data = fitbit_funcs.extract_data(sheet, [day])
            if not data.empty: 
                fitbit_funcs.refresh_sheet_tracker(tracker, data)
                print(f"{sheet} data updated for {day}.")

if __name__ == "__main__":
    testing = True
    trackers = [fitbit_funcs.BAF, fitbit_funcs.SLEEP, fitbit_funcs.EMOODS]
    sheets = ['baf', 'sleep', 'emoods']

    if testing: 
        date_range = ['2020-05-01', '2020-05-02']
    else:
        date_range = fitbit_funcs.set_date_range(fitbit_funcs.BAF)

    main(trackers, sheets, date_range)

