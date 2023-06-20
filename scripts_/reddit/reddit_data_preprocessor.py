import pandas as pd

def process_text(reddit_content):
    reddit_words = []
    for word in reddit_content.split(' '):
        if word.startswith('/u/') and len(word) > 3:
            word = '/u/user'
        elif word.startswith('http'):
            word = "http"
        reddit_words.append(word)
    reddit_proc = " ".join(reddit_words)
    return reddit_proc

if __name__ == "__main__":
    df = pd.read_csv("raw_reddit_nft_data.csv")
    df['processed_text'] = df['Content'].apply(process_text)
    df.to_csv('reddit_nft_data.csv', index=False)