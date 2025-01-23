import requests
import json
import os

# Configuration
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

url = "https://api.twitter.com/2/tweets/search/recent"
params = {
    "query": "(China OR Taiwan OR Indo-Pacific OR South China Sea) (movement OR events OR activity OR military OR navy) -is:retweet lang:en",
    "max_results": 100,
    "tweet.fields": "id,text,created_at,author_id",
}
headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}

def fetch_tweets():
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        tweets = response.json().get("data", [])
        return tweets
    except requests.exceptions.RequestException as e:
        print(f"Error during API call: {e}")
        return []

def save_tweets(tweets):
    if not tweets:
        print("No tweets fetched. raw_tweets.json will not be created.")
        return False  # Indicate the file was not created
    with open("raw_tweets.json", "w") as f:
        json.dump(tweets, f, indent=4)
    print(f"{len(tweets)} tweets saved to raw_tweets.json.")
    return True  # Indicate the file was created

if __name__ == "__main__":
    tweets = fetch_tweets()
    file_created = save_tweets(tweets)
    if not file_created:
        print("Skipping further processing since no data was saved.")
