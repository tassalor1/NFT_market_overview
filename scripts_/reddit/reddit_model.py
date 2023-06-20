import os
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pickle

def load_model():
    nltk.download('vader_lexicon')
    return SentimentIntensityAnalyzer()

def save_sentiment(sentiment, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(sentiment, file)
    print("Sentiment has been pickled")


def overall_score(sentiment):
    if sentiment >= 0.05:
        return 'Positive'
    elif sentiment <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

if __name__ == "__main__":
    df = pd.read_csv("reddit_nft_data.csv")
    sia = load_model()
    text = " ".join(df['processed_text'])
    sentiment = sia.polarity_scores(text)
    overall_sentiment = overall_score(sentiment['compound'])
    directory = 'C:\\Users\\Connor\\Desktop\\Coding\\nft_market_a\\models'
    file_path = os.path.join(directory, 'reddit_sentiment_model.pkl')
    save_sentiment(sentiment, file_path)
