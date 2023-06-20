import os
from dotenv import load_dotenv
import praw

def main():
    load_enviroment()
    unwanted_keywords = ['giveaway', 'Like', 'RT', 'Giveaways', 'follow', 'free mint', 'trending', 'Sold', 'win']


def load_enviroment():
    load_dotenv()

    reddit = praw.Reddit(
       client_id=os.getenv("REDDIT_CLIENT_ID"),
       client_secret=os.getenv("REDDIT_SECRET"),
       user_agent='tassalor_sentiment'
    )


def fetch_filtered_posts(unwanted_keywords):
    # Fetches any post that mentions nft
    hot_posts = reddit.subreddit('all').search('nft', limit=100)
    for post in hot_posts:
        # Check both the post's title and selftext (content) for unwanted keywords
        if not any(unwanted_keyword.lower() in post.title.lower() or unwanted_keyword.lower() in post.selftext.lower()
                   for unwanted_keyword in unwanted_keywords):
            print(post.title)
            # Pulls the comments of that post
            post.comments.replace_more(limit=None)
            for comment in post.comments.list()[1:]: # Skips the first comment as this is normally a bot
                print(comment.body)

