def main():
    load_environment_variables()

    api = authenticate_tweepy()

    account_username = "DegenerateNews"
    keywords = "nft"
    unwanted_keywords = ['giveaway', 'Like', 'RT', 'Giveaways', 'follow', 'free mint', 'trending',
                         'Price Action Analysi', 'Sold', 'win']
    min_age_account = 30

    user_tweets = fetch_user_tweets(api, account_username)
    filtered_tweets = fetch_filtered_tweets(api, keywords, unwanted_keywords, min_age_account, account_username)

    combined_tweets = filtered_tweets
    combined_tweets = combined_tweets[:]

    file_write(combined_tweets)

    print(f"user_tweets length: {len(user_tweets)}")
    print(f"filtered_tweets length: {len(filtered_tweets)}")
    # print_tweets(combined_tweets)

    """
    #############################################################
    Model
    #############################################################
    """
    # Read file to perform cleaning and sentiment analysis
    df = pd.read_csv("C:\\Users\\Connor\\Desktop\\Coding\\nft_market_a\\scripts_\\twitter_nft_timeline.csv")

    # Function to clean words up in data
    def process_text(tweet):
        tweet_words = []
        for word in tweet.split(' '):
            if word.startswith('@') and len(word) > 1:  # Converts their username to '@user'
                word = '@user'
            elif word.startswith('http'):  # Converts website address to 'http'
                word = "http"
            tweet_words.append(word)
        tweet_proc = " ".join(tweet_words)
        return tweet_proc

    # Create new column
    df['processed_text'] = df['Text'].apply(process_text)

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


    directory = 'C:\\Users\\Connor\\Desktop\\Coding\\nft_market_a'

    # Save the sentiment model in the specified directory
    file_path = os.path.join(directory, 'twitter_sentiment_model.pkl')
    with open(file_path, 'wb') as file:
        pickle.dump(sentiment, file)
        print("file has been pickled")


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
# Redundant for now, till I find a good account that keep the integrity of the tweets
def fetch_user_tweets(api, account_username):
    count = 300
    total_tweets = 300
    user_tweets = []
    for tweet in tweepy.Cursor(api.user_timeline,  count=count, screen_name=account_username, tweet_mode="extended"
                               ).items(total_tweets):
        user_tweets.append(tweet)
    return user_tweets


# Fetch tweets containing specific keywords and filter out tweets containing unwanted keywords
def fetch_filtered_tweets(api, keywords, unwanted_keywords, min_age_account, account_username):
    count = 300
    total_tweets = 2000
    account_age = 30
    current_date = datetime.now(pytz.utc)
    tweets = []
    filtered_tweets = []
    unique_tweet_texts = set()

    # Filtering tweets with only specific words
    for tweet in tweepy.Cursor(api.search_tweets, q=keywords, count=count, tweet_mode="extended", lang="en").items(
            total_tweets):

        # Check if rt and not a duplicate
        if not tweet.full_text.lower().startswith("rt") and tweet.full_text not in unique_tweet_texts:
            tweets.append(tweet)
            unique_tweet_texts.add(tweet.full_text)


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