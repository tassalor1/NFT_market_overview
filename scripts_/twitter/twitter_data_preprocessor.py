import pandas as pd

def process_text(tweet):
    tweet_words = []
    for word in tweet.split(' '):
        if word.startswith('@') and len(word) > 1:
            word = '@user'
        elif word.startswith('http'):
            word = "http"
        tweet_words.append(word)
    tweet_proc = " ".join(tweet_words)
    return tweet_proc

if __name__ == "__main__":
    df = pd.read_csv("raw_twitter_nft_data.csv")
    df['processed_text'] = df['Text'].apply(process_text)
    df.to_csv('twitter_nft_data.csv', index=False)
