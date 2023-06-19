import os
from dotenv import load_dotenv
import praw
load_dotenv()
reddit = praw.Reddit(
   client_id=os.getenv("REDDIT_CLIENT_ID"),
   client_secret=os.getenv("REDDIT_SECRET"),
   user_agent='tassalor_sentiment'
)

hot_posts = reddit.subreddit('NFT').hot(limit=10)
for post in hot_posts:
    print(post.title)
