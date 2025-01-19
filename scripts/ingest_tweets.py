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

if __name__ == "__main__":
    tweets = fetch_tweets()
    with open("raw_tweets.json", "w") as f:
        json.dump(tweets, f, indent=4)
    print("Tweets saved to raw_tweets.json")
