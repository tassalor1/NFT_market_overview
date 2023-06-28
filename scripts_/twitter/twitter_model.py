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

def get_sentiment(model, text):
    return model.polarity_scores(text)

def overall_score(sentiment):
    if sentiment >= 0.05:
        return 'Positive'
    elif sentiment <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

if __name__ == "__main__":
    df = pd.read_csv('twitter_nft_data.csv') # Read csv data
    text = " ".join(df['processed_text']) # Join data
    model = load_model()
    sentiment = get_sentiment(model, text) # Load model
    overall_sentiment = overall_score(sentiment['compound']) # Final model output
    print(f"Twitter sentiment is: {overall_sentiment}")
    directory = 'C:\\Users\\Connor\\Desktop\\Coding\\nft_market_a'
    file_path = os.path.join(directory, 'twitter_sentiment_model.pkl')
    save_sentiment(sentiment, file_path)
