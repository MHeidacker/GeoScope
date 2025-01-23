import requests
import json
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("tweet_streaming.log"),
        logging.StreamHandler()
    ]
)

# Load Foundry token
FOUNDRY_TOKEN = os.getenv("TWEET_FOUNDRY_TOKEN")

if not FOUNDRY_TOKEN:
    logging.error("Foundry token is not set. Please set the TWEET_FOUNDRY_TOKEN environment variable.")
    exit(1)

# Path to raw_tweets.json file
raw_tweets_file = "raw_tweets.json"

# Load raw_tweets.json file
try:
    with open(raw_tweets_file, "r") as file:
        raw_tweets = json.load(file)
    logging.info(f"Successfully loaded {len(raw_tweets)} tweets from {raw_tweets_file}.")
except Exception as e:
    logging.error(f"Error reading raw_tweets.json: {e}")
    exit(1)

# Ensure raw_tweets is a list of dictionaries
if not isinstance(raw_tweets, list):
    logging.error("raw_tweets.json must contain a list of JSON objects.")
    exit(1)

# Prepare data to match the required schema
stream_data = []
for i, tweet in enumerate(raw_tweets):
    try:
        formatted_tweet = {
            "edit_history_tweet_ids": tweet.get("edit_history_tweet_ids", ["value"]),
            "id": tweet.get("id", "value"),
            "text": tweet.get("text", "value"),
            "author_id": tweet.get("author_id", "value"),
            "created_at": tweet.get("created_at", "value"),
        }
        stream_data.append({"value": formatted_tweet})
        logging.debug(f"Tweet {i+1} formatted successfully.")
    except Exception as e:
        logging.warning(f"Skipping tweet {i+1} due to formatting error: {e}")

# Ensure at least one valid tweet is prepared
if not stream_data:
    logging.error("No valid tweets to stream. Exiting.")
    exit(1)

# Define Foundry streaming API endpoint
post_uri = "https://heidacker.usw-3.palantirfoundry.com/stream-proxy/api/streams/ri.foundry.main.dataset.b791758c-9239-4ecb-ac75-6fbaca864bf4/views/ri.foundry-streaming.main.view.54406e4b-71ae-4ede-88b4-38662b962ad6/jsonRecords"

# Send POST request
try:
    response = requests.post(
        post_uri,
        data=json.dumps(stream_data),
        headers={
            "Authorization": "Bearer " + FOUNDRY_TOKEN,
            "Content-Type": "application/json",
        },
    )
    if response.status_code == 200:
        logging.info("Data streamed successfully to Foundry.")
    else:
        logging.error(f"Failed to stream data: {response.status_code} {response.reason}")
        logging.debug(f"Response text: {response.text}")

except Exception as e:
    logging.error(f"Error making POST request: {e}")
