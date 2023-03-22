import os
import json
from datetime import datetime
import csv
import pytz

# set the path to your directory containing the JSON files
path = 'submission_threads'
csv_file = "csv_posts/aw_submissions.csv"
# create a list of all JSON files in the directory
json_files = [pos_json for pos_json in os.listdir(path) if pos_json.endswith('.json')]

# count the number of JSON files in the directory
num_files = len(json_files)

# initialize a variable to keep track of the total number of JSON objects
total_objects = 0
comment_count = 0

# read the csv file
# open the CSV file and count the number of rows
with open(csv_file, "r") as f:
    reader = csv.reader(f)
    total = sum(1 for row in reader)

# local_tz = pytz.timezone('Europe/London')
# with open(csv_file, "r") as f:
#     reader = csv.reader(f)
#     header_row = next(reader)  # skip header row
#
#     oldest_row = None
#     youngest_row = None
#
#     for row in reader:
#         created_utc = int(row[header_row.index("created_utc")])
#         created_datetime = datetime.fromtimestamp(created_utc)
#
#         if oldest_row is None or created_datetime < oldest_row_datetime:
#             oldest_row = row
#             oldest_row_datetime = created_datetime
#
#         if youngest_row is None or created_datetime > youngest_row_datetime:
#             youngest_row = row
#             youngest_row_datetime = created_datetime
#

# loop through each JSON file and count the number of objects in each file
for file in json_files:
    with open(os.path.join(path, file), 'r') as f:
        data = json.load(f)
        num_objects = len(data)
        total_objects += num_objects
        # calculate the progress percentage
        progress = int(total_objects / total * 100)
        for json_object in data:
            comments = json_object.get('comments', [])
            for comment in comments:
                comment_count += 1

# get the current date and time
now = datetime.now()
date_time = now.strftime("%m/%d/%Y %H:%M:%S")

# write the log file
with open('Log.txt', 'a') as log_file:
    log_file.write(f'{date_time}: Number of JSON files: {num_files}\n')
    log_file.write(f'{date_time}: Total number of JSON Posts Collected: {total_objects} ({progress}%)\n')
    log_file.write(f"{date_time}: Number of comments Collected: {comment_count}\n")
    log_file.write("\n")
