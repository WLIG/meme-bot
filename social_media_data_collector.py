import tweepy
import json
import time

class SocialMediaDataCollector:
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True)
        print("Twitter API initialized.")

    def search_tweets(self, query, count=100):
        print(f"Searching tweets for query: '{query}'...")
        tweets = []
        try:
            for tweet in tweepy.Cursor(self.api.search_tweets, q=query, lang="en", tweet_mode='extended').items(count):
                tweets.append({
                    "id": tweet.id_str,
                    "created_at": tweet.created_at.isoformat(),
                    "text": tweet.full_text,
                    "user": {
                        "id": tweet.user.id_str,
                        "screen_name": tweet.user.screen_name,
                        "followers_count": tweet.user.followers_count,
                        "friends_count": tweet.user.friends_count,
                        "verified": tweet.user.verified
                    },
                    "retweet_count": tweet.retweet_count,
                    "favorite_count": tweet.favorite_count,
                    "hashtags": [tag["text"] for tag in tweet.entities["hashtags"]],
                    "mentions": [mention["screen_name"] for mention in tweet.entities["user_mentions"]]
                })
            print(f"Collected {len(tweets)} tweets for query '{query}'.")
        except tweepy.TweepyException as e:
            print(f"Error searching tweets: {e}")
        return tweets

    def get_user_timeline(self, screen_name, count=100):
        print(f"Getting user timeline for @{screen_name}...")
        tweets = []
        try:
            for tweet in tweepy.Cursor(self.api.user_timeline, screen_name=screen_name, tweet_mode='extended').items(count):
                tweets.append({
                    "id": tweet.id_str,
                    "created_at": tweet.created_at.isoformat(),
                    "text": tweet.full_text,
                    "user": {
                        "id": tweet.user.id_str,
                        "screen_name": tweet.user.screen_name,
                        "followers_count": tweet.user.followers_count,
                        "friends_count": tweet.user.friends_count,
                        "verified": tweet.user.verified
                    },
                    "retweet_count": tweet.retweet_count,
                    "favorite_count": tweet.favorite_count,
                    "hashtags": [tag["text"] for tag in tweet.entities["hashtags"]],
                    "mentions": [mention["screen_name"] for mention in tweet.entities["user_mentions"]]
                })
            print(f"Collected {len(tweets)} tweets from @{screen_name}.")
        except tweepy.TweepyException as e:
            print(f"Error getting user timeline: {e}")
        return tweets

async def main():
    # Replace with your actual Twitter API credentials
    # It is highly recommended to load these from environment variables or a secure config management system
    consumer_key = "YOUR_CONSUMER_KEY"
    consumer_secret = "YOUR_CONSUMER_SECRET"
    access_token = "YOUR_ACCESS_TOKEN"
    access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

    collector = SocialMediaDataCollector(consumer_key, consumer_secret, access_token, access_token_secret)

    # Example usage:
    # Search for tweets mentioning a specific meme coin
    meme_coin_tweets = collector.search_tweets("DOGE OR SHIB", count=10)
    print("\nMeme Coin Tweets:")
    print(json.dumps(meme_coin_tweets, indent=2))

    # Get timeline of a crypto KOL
    # kol_tweets = collector.get_user_timeline("cz_binance", count=5)
    # print("\nCZ Binance Tweets:")
    # print(json.dumps(kol_tweets, indent=2))

if __name__ == "__main__":
    asyncio.run(main())


