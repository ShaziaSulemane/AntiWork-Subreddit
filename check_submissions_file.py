import pandas as pd
import glob
from datetime import datetime

# create an empty list to store unique values
unique_ids = []
now = datetime.now()
date_time = now.strftime("%m/%d/%Y %H:%M:%S")
dateforlog = now.strftime("%m_%d_%Y")

existing_posts = []
log_filename = "Log_" + dateforlog + ".txt"

with open(f"Logs/{log_filename}", "a") as log_file:
    log_file.write(f"{date_time}: Analysis of CSV post files\n")
    log_file.close()

# get a list of all csv files in the folder
csv_files = glob.glob('aw_posts/*.csv')

# loop through each csv file and extract unique ids
for file in csv_files:
    # read csv file into a pandas dataframe
    df = pd.read_csv(file)
    # extract the 'id' column and add to unique_ids list
    unique_ids.extend(df['id'].unique())
    with open(f"Logs/{log_filename}", "a") as log_file:
        log_file.write(f"{date_time}: {file.title()} has {len(df['id'].tolist())} lines\n")
        log_file.close()

# convert unique_ids list to a set to remove duplicates
unique_ids = list(set(unique_ids))

with open(f"Logs/{log_filename}", "a") as log_file:
    log_file.write(f"{date_time}: All files have {len(unique_ids)} unique ids\n")
    log_file.close()
