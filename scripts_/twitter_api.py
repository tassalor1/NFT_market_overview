import tweepy
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import pytz


def main():
    load_environment_variables()

    api = authenticate_tweepy()

    account_username = "DegenerateNews"
    keywords = "nft OR NFT OR BAYC OR opensea OR blur"
    unwanted_keywords = ['giveaway', 'Like', 'RT', 'Giveaways', 'follow', 'free mint']
    min_age_account = 30

    user_tweets = fetch_user_tweets(api, account_username)
    filtered_tweets = fetch_filtered_tweets(api, keywords, unwanted_keywords, min_age_account, account_username)

    combined_tweets = filtered_tweets + user_tweets

    print_tweets(combined_tweets)


# Load environment variables and set global variables for API keys and tokens
def load_environment_variables():
    load_dotenv()
    global consumer_key, consumer_secret, access_token, access_token_secret
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")


# Authenticate tweepy with the API keys and tokens and return the API object
# Waits till rate limit is refereshed
def authenticate_tweepy():
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    return tweepy.API(auth, wait_on_rate_limit=True)


# Fetch tweets from the specified user's timeline and return a list of full tweet texts
def fetch_user_tweets(api, account_username):
    user_tweets = []
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=account_username, tweet_mode="extended").items():
        user_tweets.append(tweet.full_text)
    return user_tweets


# Fetch tweets containing specific keywords and filter out tweets containing unwanted keywords
def fetch_filtered_tweets(api, keywords, unwanted_keywords, min_age_account, account_username):
    count = 100
    total_tweets = 10
    account_age = 30
    current_date = datetime.now(pytz.utc)
    tweets = []
    filtered_tweets = []

    # Filtering tweets with only specific words
    for tweet in tweepy.Cursor(api.search_tweets, q=keywords, count=count, tweet_mode="extended", lang="en").items(total_tweets):
        tweets.append(tweet)

    # Filtering tweets of spam words
    for tweet in tweets:
        if not any(unwanted_keyword.lower() in tweet.full_text.lower() for unwanted_keyword in unwanted_keywords):
            filtered_tweets.append(tweet)

    # Filtering tweets with account age < 30
    age_filter = []
    for tweet in filtered_tweets:
        if (current_date - tweet.user.created_at) >= timedelta(days=min_age_account):
            age_filter.append(tweet)

    # Filter spam @'s
    at_spam = []
    for tweet in age_filter:
        if tweet.full_text.count('@') >= 3:
            at_spam.append(tweet.full_text)

    # Fetch all tweets from specified account
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=account_username, tweet_mode="extended").items():
        at_spam.append(tweet.full_text)

    return at_spam


# Print fetched tweets
def print_tweets(combined_tweets):
    for tweet in combined_tweets:
        print(tweet)
        print('-' * 80)


if __name__ == "__main__":
    main()