import datetime as dt
import json
import time
import prawcore
import praw
from pushshift_py import PushshiftAPI
from tqdm import tqdm

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

import pandas as pd

# read the csv file into a pandas dataframe
df = pd.read_csv('aw_submissions.csv')
posts = []
# extract the 'id' column as a list
id_list = df['id'].tolist()
id_list = id_list[(3348+2326+536+344+3302+1891+4111+139+514+689+1922+1055+3648+2976+5771+1648+833+1875+1509+149):]

start_time = time.time()
for submission_id in tqdm(id_list):
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
    with open("submissions_20.json", "w") as f:
        json.dump(posts, f)
        f.close()
