from datetime import datetime
import datetime as dt
import json
import time
import prawcore
import praw
from pushshift_py import PushshiftAPI
from tqdm import tqdm
import os
import pandas as pd

# https://pypi.org/project/pushshift.py/

CLIENT_ID = 'bMzGtUxCuPs6LeXUAqEFrA'
CLIENT_SECRET = 'Uq0lcNjjDxvAYg8ub4ytKgjVdF-FMQ'
USER_AGENT = 'NTIWORK/1.0'
USERNAME = 'anEngineerNotAFan'
PASSWORD = 'mwXFiV8R7EG3fht'
redirect_uri = 'http://localhost:8000'
subreddit_name = 'antiwork'

print("start")

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
    username=USERNAME,
    password=PASSWORD
)

api = PushshiftAPI(reddit)

# read the csv file into a pandas dataframe
df = pd.read_csv('aw_submissions.csv')
posts = []
# extract the 'id' column as a list
id_list = df['id'].tolist()
i = 0
start_time = time.time()
total = len(id_list)
fetched = 0

now = datetime.now()
date_time = now.strftime("%m/%d/%Y %H:%M:%S")
dateforlog = now.strftime("%m_%d_%Y")

existing_posts = []
log_filename = "Log_" + dateforlog + ".txt"
output_file = "posts.json"

with open(f"Logs/{log_filename}", "a") as log_file:
    log_file.write(f"{date_time}: Started Script\n")
    log_file.close()

for submission_id in tqdm(id_list):

    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y %H:%M:%S")

    if os.stat(output_file).st_size == 0:
        existing_posts = []
    else:
        with open(output_file, "r") as f:
            existing_posts = json.load(f)

    fetched = len(existing_posts)
    if any(existing_post['id'] == submission_id for existing_post in existing_posts):
        with open(f"Logs/{log_filename}", "a") as log_file:
            log_file.write(f"{date_time}:Skipping post with ID {submission_id} because it already exists in "
                           f"the file. \n")
            log_file.close()
        continue

    post = reddit.submission(id=submission_id)
    comments = []
    post.comments.replace_more(limit=None)
    for comment in post.comments.list():
        if comment is not None:
            comments.append({
                "id": comment.id,
                "author": comment.author.name if comment.author else "",
                "body": comment.body,
                "created": comment.created,
                "parent_id": comment.parent_id,
                "link_id": comment.link_id,
                "score": comment.score,
            })
            time.sleep(0.2)
    posts.append({
        "id": post.id,
        "title": post.title,
        "author": post.author.name if post.author else "",
        "score": post.score,
        "url": post.url,
        "num_comments": post.num_comments,
        "self_text": post.selftext,
        "created": post.created,
        "comments": comments
    })

    with open(output_file, "w") as f:
        json.dump(existing_posts + posts, f)
        with open(f"Logs/{log_filename}", "a") as log_file:
            log_file.write(f'{date_time}: Fetched post {post.id} Progress: {int(fetched / total * 100)}% Fetched: {fetched} Total Posts: {total}\n')
            log_file.close()
        f.close()
