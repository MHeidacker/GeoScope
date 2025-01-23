import requests
import json
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("reddit_streaming.log"),
        logging.StreamHandler()
    ]
)

# Load Foundry token
FOUNDRY_TOKEN = os.getenv("REDDIT_FOUNDRY_TOKEN")

if not FOUNDRY_TOKEN:
    logging.error("Foundry token is not set. Please set the REDDIT_FOUNDRY_TOKEN environment variable.")
    exit(1)

# Path to file
reddit_comments_file = "reddit_comments.json"

# Load json file
try:
    with open(reddit_comments_file, "r") as file:
        reddit_comments = json.load(file)
    logging.info(f"Successfully loaded {len(reddit_comments)} comments from {reddit_comments_file}.")
except Exception as e:
    logging.error(f"Error reading reddit_comments.json: {e}")
    exit(1)

# Ensure reddit_comments is a list of dictionaries
if not isinstance(reddit_comments, list):
    logging.error("reddit_comments.json must contain a list of JSON objects.")
    exit(1)

# Prepare data to match the required schema
stream_data = []
for i, comment in enumerate(reddit_comments):
    try:
        formatted_comment = {
            "id": comment.get("id", "value"),
            "body": comment.get("body", "value"),
            "date": comment.get("date", "value"),
            "submission_title": comment.get("submission_title", "value")
        }
        stream_data.append({"value": formatted_comment})
        logging.debug(f"Comment {i + 1} formatted successfully.")
    except Exception as e:
        logging.warning(f"Skipping comment {i + 1} due to formatting error: {e}")

# Ensure at least one valid comment is prepared
if not stream_data:
    logging.error("No valid comments to stream. Exiting.")
    exit(1)

# Define Foundry streaming API endpoint
post_uri = "https://heidacker.usw-3.palantirfoundry.com/stream-proxy/api/streams/ri.foundry.main.dataset.638cf8db-ec0a-4175-92ae-d4730817f1ba/views/ri.foundry-streaming.main.view.eedd83d8-64e3-43e6-8ef5-fd869479480a/jsonRecords"

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
