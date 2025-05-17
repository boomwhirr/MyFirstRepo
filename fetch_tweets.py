import os
import tweepy
from textblob import TextBlob


def authenticate():
    """Authenticate with the Twitter API using credentials from environment variables."""
    api_key = os.environ.get("TWITTER_API_KEY")
    api_secret = os.environ.get("TWITTER_API_SECRET")
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

    if not all([api_key, api_secret, access_token, access_token_secret]):
        raise EnvironmentError(
            "Twitter API credentials not fully provided in environment variables"
        )

    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api


def fetch_tweets(api, query, count=100):
    """Fetch the latest tweets matching the query."""
    tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en", tweet_mode="extended").items(count)
    return list(tweets)


def analyze_sentiment(text):
    """Return the polarity score of the text using TextBlob."""
    analysis = TextBlob(text)
    return analysis.sentiment.polarity


def main():
    api = authenticate()
    query = os.environ.get("STOCK_QUERY", "$AAPL")
    tweets = fetch_tweets(api, query, count=100)
    for tweet in tweets:
        text = tweet.full_text
        sentiment = analyze_sentiment(text)
        clean_text = text.replace("\n", " ")
        print(f"{sentiment:.3f}\t{clean_text}")


if __name__ == "__main__":
    main()
