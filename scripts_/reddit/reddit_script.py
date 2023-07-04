import os
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pickle
import time
from dotenv import load_dotenv
import praw
import csv


def main():

    start_time = time.time() # Start timer
    reddit = load_enviroment()
    unwanted_keywords = ['giveaway', 'Like', 'RT', 'Giveaways', 'follow', 'free mint', 'trending', 'Sold', 'win']
    filtered_posts_and_comments  = fetch_filtered_posts(reddit, unwanted_keywords)
    write_to_csv(filtered_posts_and_comments)
    end_time = time.time() # End timer

    print(f'Time Taken: {end_time - start_time} seconds')
    print(f"filtered_posts_and_comments: {len(filtered_posts_and_comments)}")

    """
       #############################################################
       Model
       #############################################################
       """
    # Read file to perform cleaning and sentiment analysis
    df = pd.read_csv("C:\\Users\\Connor\\Desktop\\Coding\\nft_market_a\\data\\reddit_nft_data.csv")

    # Function to clean words up in data
    def process_text(reddit_content):
        reddit_words = []
        for word in reddit_content.split(' '):
            if word.startswith('/u/') and len(word) > 3:  # Converts Reddit username to '/u/user'
                word = '/u/user'
            elif word.startswith('http'):  # Converts website address to 'http'
                word = "http"
            reddit_words.append(word)
        reddit_proc = " ".join(reddit_words)
        return reddit_proc

    # Create new column
    df['processed_text'] = df['Content'].apply(process_text)

    # Load Model
    nltk.download('vader_lexicon')  # Vader model

    sia = SentimentIntensityAnalyzer()

    text = " ".join(df['processed_text'])  # Join all text toghether so it gives a score as one

    sentiment = sia.polarity_scores(text)

    """
    The VADER Sentiment Analysis provides us with a compound score, which serves as a comprehensive measure of the
    text's sentiment. This compound score lies within a range of -1 to 1. Here, -1 signifies extremely negative sentiment,
    while 1 represents extremely positive sentiment. To interpret this continuous score in a more categorical form,
    we will construct a function. This function will assign each score to a corresponding sentiment
    category: 'negative', 'neutral', or 'positive', based on its value within the -1 to 1 range.
    """

    # Function to find overall sentiment as compound score by itself doesnt mean much
    # I think having neutral around -0.05 to 0.05 is the best range for its value
    def overall_score(sentiment):
        if sentiment >= 0.05:
            return 'Positive'
        elif sentiment <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'

    overall_sentiment = overall_score(sentiment['compound'])
    print(overall_sentiment)

    directory = 'C:\\Users\\Connor\\Desktop\\Coding\\nft_market_a\\data'

    # Save the sentiment model in the specified directory
    file_path = os.path.join(directory, 'reddit_sentiment_model1.pkl')
    with open(file_path, 'wb') as file:
        pickle.dump(sentiment, file)
        print("file has been pickled")


def load_enviroment():
    load_dotenv()

    reddit = praw.Reddit(
       client_id=os.getenv("REDDIT_CLIENT_ID"),
       client_secret=os.getenv("REDDIT_SECRET"),
       user_agent='tassalor_sentiment'
    )
    return reddit

# Fetch data
def fetch_filtered_posts(reddit, unwanted_keywords):
    results = []
    # Fetches any post that mentions nft
    hot_posts = reddit.subreddit('all').search('nft', limit=10)
    for post in hot_posts:
        # Check both the post's title and selftext (content) for unwanted keywords
        if not any(unwanted_keyword.lower() in post.title.lower() or unwanted_keyword.lower() in post.selftext.lower()
                   for unwanted_keyword in unwanted_keywords):
            results.append(("Post", post.id, post.title))

            # Pulls the comments of that post
            post.comments.replace_more(limit=None)
            for comment in post.comments.list()[1:]: # Skips the first comment as this is normally a bot
                results.append(("Comment", post.id, comment.body))

    return results

def write_to_csv(filtered_posts_and_comments):
    with open('C:\\Users\\Connor\\Desktop\\Coding\\nft_market_a\\data\\reddit_nft_data.csv', 'w',
              newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Write the header row
        writer.writerow(["Type", "Post ID", "Content"])

        # Write the post and comment data
        for item in filtered_posts_and_comments:
            writer.writerow(item)

if __name__ == "__main__":
    main()