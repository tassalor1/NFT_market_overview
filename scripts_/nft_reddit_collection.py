import os
from dotenv import load_dotenv
import praw
import csv

def main():
    reddit = load_enviroment()
    unwanted_keywords = ['giveaway', 'Like', 'RT', 'Giveaways', 'follow', 'free mint', 'trending', 'Sold', 'win']
    filtered_posts_and_comments  = fetch_filtered_posts(reddit, unwanted_keywords)
    file_write(filtered_posts_and_comments)
    print(f"filtered_posts_and_comments: {len(filtered_posts_and_comments)}")

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
    # Fetches any post that mentions nft
    hot_posts = reddit.subreddit('all').search('nft', limit=10)
    for post in hot_posts:
        # Check both the post's title and selftext (content) for unwanted keywords
        if not any(unwanted_keyword.lower() in post.title.lower() or unwanted_keyword.lower() in post.selftext.lower()
                   for unwanted_keyword in unwanted_keywords):
            results.append(post.title)

            # Pulls the comments of that post
            post.comments.replace_more(limit=None)
            for comment in post.comments.list()[1:]: # Skips the first comment as this is normally a bot
                results.append(comment.body)

    return results

def file_write(filtered_posts_and_comments):
    with open('reddit_nft_posts_comments', 'w', newline='', encoding='utf-8') as f:

        writer = csv.writer(f)

        # Header row
        writer.writerow(["Post Title", "Post Content", "Post ID", "Subreddit", "Author", "Post Date", "Comment", "Comment ID", "Comment Date"])

        for post_id, post_details in filtered_posts_and_comments.items():
            for comment in post_details['comments']:
                writer.writerow([
                    post_id,
                    post_details['post_title'],
                    post_details['post_content'],
                    post_details['subreddit'],
                    post_details['author'],
                    post_details['post_date'],
                    comment['comment_id'],
                    comment['comment_content'],
                    comment['comment_date'],
                ])
if __name__ == "__main__":
    main()
