import praw
import json
import os
from datetime import datetime

# Reddit API credentials from environment variables
client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_CLIENT_SECRET")
user_agent = os.getenv("REDDIT_USER_AGENT")
username = os.getenv("REDDIT_USERNAME")
password = os.getenv("REDDIT_PASSWORD")

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password
)

def fetch_comments(keywords, subreddits, limit=50, comment_limit=20):
    print(f"Searching for posts containing: {keywords}")
    results = []
    for subreddit in subreddits:
        print(f"\nSearching in r/{subreddit}...")
        # Search for posts in the subreddit
        for submission in reddit.subreddit(subreddit).search(keywords, limit=limit):
            submission.comments.replace_more(limit=0)  # Flatten comment tree
            
            for comment in submission.comments[:comment_limit]:  # Limit number of comments per post
                results.append({
                    "id": comment.id,  # Unique comment ID
                    "body": comment.body,  # Comment text
                    "date": datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                    "submission_title": submission.title  # Title of the post the comment belongs to
                })
    return results

if __name__ == "__main__":
    # Define keywords and target subreddits
    keywords = "Indo-Pacific OR China OR Taiwan"
    subreddits = ["worldnews", "geopolitics", "china", "taiwan", "politics"]

    # Fetch comments
    comments = fetch_comments(keywords, subreddits, limit=50, comment_limit=20)

    # Save results to JSON file
    output_file = "reddit_comments.json"
    with open(output_file, "w") as file:
        json.dump(comments, file, indent=4)
    print(f"\nSearch complete! Results saved to {output_file}.")
