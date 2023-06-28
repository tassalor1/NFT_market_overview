import os
import csv
import tweepy
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz

def load_enviroment():
    load_dotenv()
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    return tweepy.API(auth, wait_on_rate_limit=True)

# Filtering tweets
def fetch_filtered_tweets(api, keywords, unwanted_keywords, min_age_account, account_username):
    count = 300
    total_tweets = 2000
    current_date = datetime.now(pytz.utc)
    tweets = []
    filtered_tweets = []
    unique_tweet_texts = set()


    for tweet in tweepy.Cursor(api.search_tweets, q=keywords, count=count, tweet_mode="extended", lang="en").items(total_tweets):
        if not tweet.full_text.lower().startswith("rt") and tweet.full_text not in unique_tweet_texts:
            tweets.append(tweet)
            unique_tweet_texts.add(tweet.full_text)

    for tweet in tweets:
        if not any(unwanted_keyword.lower() in tweet.full_text.lower() for unwanted_keyword in unwanted_keywords):
            filtered_tweets.append(tweet)

    age_filter = []
    for tweet in filtered_tweets:
        if (current_date - tweet.user.created_at) >= timedelta(days=min_age_account):
            age_filter.append(tweet)

    return age_filter

def write_to_csv(combined_tweets):
    with open('raw_twitter_nft_data.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Tweet ID", "Username", "User ID", "Tweet Date", "Text"])
        for tweet in combined_tweets:
            writer.writerow([tweet.id_str, tweet.user.screen_name, tweet.user.id_str, tweet.created_at, tweet.full_text])

if __name__ == "__main__":
    api = load_enviroment()
    account_username = "DegenerateNews"
    keywords = "nft"
    unwanted_keywords = ['giveaway', 'Like', 'RT', 'Giveaways', 'follow', 'free mint', 'trending', 'Price Action Analysi', 'Sold', 'win']
    min_age_account = 30
    filtered_tweets = fetch_filtered_tweets(api, keywords, unwanted_keywords, min_age_account, account_username)
    write_to_csv(filtered_tweets)
