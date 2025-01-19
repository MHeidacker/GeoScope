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

# Prepare data for Foundry streaming API
# Foundry expects a list of rows with the "value" field containing the data
stream_data = [{"value": tweet} for tweet in raw_tweets]

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
