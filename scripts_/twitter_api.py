import tweepy
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import pytz
import csv


def main():
    load_environment_variables()

    api = authenticate_tweepy()

    account_username = "DegenerateNews"
    keywords = "nft OR BAYC OR opensea OR blur OR azuki OR bored ape OR degods OR NFTs OR clone X OR NGMI " \
               "pfp OR floor price OR JPGs OR jpg OR roadmap OR wagmi"
    unwanted_keywords = ['giveaway', 'Like', 'RT', 'Giveaways', 'follow', 'free mint']
    min_age_account = 30

    user_tweets = fetch_user_tweets(api, account_username)
    filtered_tweets = fetch_filtered_tweets(api, keywords, unwanted_keywords, min_age_account, account_username)

    combined_tweets = user_tweets + filtered_tweets
    combined_tweets = combined_tweets[:100]

    file_write(combined_tweets)

    print(f"user_tweets length: {len(user_tweets)}")
    print(f"filtered_tweets length: {len(filtered_tweets)}")
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
    count = 100
    total_tweets = 100
    user_tweets = []
    for tweet in tweepy.Cursor(api.user_timeline,  count=count, screen_name=account_username, tweet_mode="extended").items(total_tweets):
        user_tweets.append(tweet)
    return user_tweets


# Fetch tweets containing specific keywords and filter out tweets containing unwanted keywords
def fetch_filtered_tweets(api, keywords, unwanted_keywords, min_age_account, account_username):
    count = 100
    total_tweets = 100
    account_age = 30
    current_date = datetime.now(pytz.utc)
    tweets = []
    filtered_tweets = []

    # Filtering tweets with only specific words
    for tweet in tweepy.Cursor(api.search_tweets, q=keywords, count=count, tweet_mode="extended", lang="en").items(
            total_tweets):
        tweets.append(tweet)

    print(f"tweets length after keyword filtering: {len(tweets)}")

    # Filtering tweets of spam words
    for tweet in tweets:
        if not any(unwanted_keyword.lower() in tweet.full_text.lower() for unwanted_keyword in unwanted_keywords):
            filtered_tweets.append(tweet)

    print(f"filtered_tweets length after spam word filtering: {len(filtered_tweets)}")

    # Filtering tweets with account age < 30
    age_filter = []
    for tweet in filtered_tweets:
        if (current_date - tweet.user.created_at) >= timedelta(days=min_age_account):
            age_filter.append(tweet)

    print(f"age_filter length after account age filtering: {len(age_filter)}")

    return age_filter


# Print fetched tweets
def print_tweets(combined_tweets):
    for tweet in combined_tweets:
        print(tweet.full_text)
        print('-' * 80)


def file_write(combined_tweets):
    with open('twitter_nft_timeline.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Write the header row
        writer.writerow(["Tweet ID", "Username", "User ID", "Tweet Date", "Text"])

        # Write the tweet data
        for tweet in combined_tweets:
            writer.writerow([tweet.id_str, tweet.user.screen_name, tweet.user.id_str, tweet.created_at, tweet.full_text])


if __name__ == "__main__":
    main()