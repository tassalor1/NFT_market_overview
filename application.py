from flask import Flask, render_template
import pickle

app = Flask(__name__)

@app.route('/')
def home():
    # Load the sentiment score from the pickle file
    with open('twitter_sentiment_model.pkl', 'rb') as file:
        sentiment = pickle.load(file)

    # Get the overall sentiment score
    overall_sentiment = overall_score(sentiment['compound'])

    return render_template('front.html', sentiment=overall_sentiment)

def overall_score(sentiment):
    if sentiment >= 0.05:
        return 'Positive'
    elif sentiment <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

if __name__ == '__main__':
    app.run()