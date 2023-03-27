# create an instance of the PushshiftAPI
from datetime import datetime
import datetime as dt
import json
import time
import praw
from pushshift_py import PushshiftAPI
import pandas as pd

api = PushshiftAPI()

# set the start date as three years ago from today
start_date = datetime.utcnow() - dt.timedelta(days=3 * 365)

# set the end date as today
end_date = datetime.utcnow()

# set the subreddit name
subreddit_name = "antiwork"

# define the time interval for each week
week = dt.timedelta(days=7)
month = dt.timedelta(days=30)

now = datetime.now()
date_time = now.strftime("%m/%d/%Y %H:%M:%S")
dateforlog = now.strftime("%m_%d_%Y")

existing_posts = []
log_filename = "Log_" + dateforlog + ".txt"
threads = []

with open(f"Logs/{log_filename}", "a") as log_file:
    log_file.write(f"{date_time}: Started Fetching Submissions\n")

# loop over each week from start_date to end_date
for i in range((end_date - start_date) // week):
    # define the date range for the current week
    week_start = start_date + i * week
    week_end = start_date + (i + 1) * week
    with open(f"Logs/{log_filename}", "a") as log_file:
        log_file.write(f"{date_time}: Fetching posts from {week_start.strftime('%m/%d/%Y %H:%M:%S')} to {week_end.strftime('%m/%d/%Y %H:%M:%S')}\n")
    # fetch the posts from the current week using PushshiftAPI
    posts = api.search_submissions(subreddit=subreddit_name,
                                   after=int(week_start.timestamp()),
                                   before=int(week_end.timestamp()),
                                   limit=None, filter=['id', 'url', 'score', 'title', 'author', 'num_comments', 'self_text', 'created'])
    list_posts = list(posts)
    with open(f"Logs/{log_filename}", "a") as log_file:
        log_file.write(f"{date_time}: Fetched {len(list_posts)} posts from {week_start.strftime('%m/%d/%Y %H:%M:%S')} to {week_end.strftime('%m/%d/%Y %H:%M:%S')}\n")

    posts_df = pd.DataFrame(list_posts)
    # construct the filename for this week's posts
    # write the posts to a JSON file
    posts_df.to_csv(f'submissions/aw_posts_{week_start}_{week_end}.csv', header=True, index=False, columns=list(posts_df.axes[1]))
    # wait for a moment to avoid hitting API limits
    time.sleep(0.2)

# print a message when the script is finished
print("Finished fetching weekly posts and saving to JSON files")
