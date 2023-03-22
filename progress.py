import os
import json
from datetime import datetime

# set the path to your directory containing the JSON files
path = 'submission_threads'

# create a list of all JSON files in the directory
json_files = [pos_json for pos_json in os.listdir(path) if pos_json.endswith('.json')]

# count the number of JSON files in the directory
num_files = len(json_files)

# initialize a variable to keep track of the total number of JSON objects
total_objects = 0

comment_count = 0

# loop through each JSON file and count the number of objects in each file
for file in json_files:
    with open(os.path.join(path, file), 'r') as f:
        data = json.load(f)
        num_objects = len(data)
        total_objects += num_objects
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
    log_file.write(f'{date_time}: Total number of JSON Posts: {total_objects}\n')
    log_file.write(f"{date_time}:Number of comments: {comment_count}\n")
    log_file.write("\n")
