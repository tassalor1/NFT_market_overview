import os
import csv
from dotenv import load_dotenv
import praw

def load_enviroment():
    load_dotenv()
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_SECRET"),
        user_agent='tassalor_sentiment'
    )
    return reddit

def fetch_filtered_posts(reddit, unwanted_keywords):
    results = []
    hot_posts = reddit.subreddit('all').search('nft', limit=10)
    for post in hot_posts:
        if not any(unwanted_keyword.lower() in post.title.lower() or unwanted_keyword.lower() in post.selftext.lower()
                for unwanted_keyword in unwanted_keywords):
            results.append(("Post", post.id, post.title))
            post.comments.replace_more(limit=None)
            for comment in post.comments.list()[1:]:
                results.append(("Comment", post.id, comment.body))
    return results

def write_to_csv(filtered_posts_and_comments, file_path):
    with open('raw_reddit_nft_data.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Type", "Post ID", "Content"])
        for item in filtered_posts_and_comments:
            writer.writerow(item)

if __name__ == "__main__":
    reddit = load_enviroment()
    unwanted_keywords = ['giveaway', 'Like', 'RT', 'Giveaways', 'follow', 'free mint', 'trending', 'Sold', 'win']
    filtered_posts_and_comments  = fetch_filtered_posts(reddit, unwanted_keywords)
    write_to_csv(filtered_posts_and_comments, 'C:\\Users\\Connor\\Desktop\\Coding\\nft_market_a\data\\raw_data')
