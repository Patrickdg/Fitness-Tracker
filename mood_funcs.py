# LIBRARIES
import os
import pandas as pd
import zipfile
from fitbit_funcs import *

# DECLARATIONS
emoods_path = r'C:\Users\Patrick\OneDrive\TRAINING\FITNESS_DASHBOARD\emoods-data'

# FUNCTIONS
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

    old_entries = moods_data.iloc[:,1].isin(EMOODS.col_values(1)[1:])
    moods_data = moods_data[~old_entries].iloc[:,1:7]

    return moods_data
