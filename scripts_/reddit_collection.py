import os

import praw

reddit = praw.Reddit(
   client_id = os.getenv("REDDIT_CLIENT_ID"),
   client_secret = os.getenv("REDDIT_SECRET"),
   user_agent='tassalor1'
)

hot_posts = reddit.subreddit('NFt').hot(limit=10)
for post in hot_posts:
    print(post.title)
