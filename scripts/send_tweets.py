import requests
import json
import os

# Load Foundry token from environment variable
FOUNDRY_TOKEN = os.getenv("TWEET_FOUNDRY_TOKEN")

# Path to your raw_tweets.json file
raw_tweets_file = "raw_tweets.json"

# Load raw_tweets.json file
try:
    with open(raw_tweets_file, "r") as file:
        raw_tweets = json.load(file)
except Exception as e:
    print(f"Error reading raw_tweets.json: {e}")
    exit(1)

# Ensure raw_tweets is a list of dictionaries
if not isinstance(raw_tweets, list):
    print("Error: raw_tweets.json must contain a list of JSON objects.")
    exit(1)

# Prepare data to match the required schema
stream_data = []
for tweet in raw_tweets:
    formatted_tweet = {
        "edit_history_tweet_ids": tweet.get("edit_history_tweet_ids", ["value"]),
        "id": tweet.get("id", "value"),
        "text": tweet.get("text", "value"),
        "author_id": tweet.get("author_id", "value"),
        "created_at": tweet.get("created_at", "value"),
    }
    stream_data.append({"value": formatted_tweet})

# Define Foundry streaming API endpoint
post_uri = "https://heidacker.usw-3.palantirfoundry.com/stream-proxy/api/streams/ri.foundry.main.dataset.b791758c-9239-4ecb-ac75-6fbaca864bf4/views/ri.foundry-streaming.main.view.54406e4b-71ae-4ede-88b4-38662b962ad6/jsonRecords"

# Send POST request
try:
    response = requests.post(
        post_uri,
        data=json.dumps(stream_data),  # Send the processed stream data
        headers={
            "Authorization": "Bearer " + FOUNDRY_TOKEN,
            "Content-Type": "application/json",
        },
    )

    # Print response details
    print(response.status_code, response.reason, response.text)

except Exception as e:
    print(f"Error making POST request: {e}")
