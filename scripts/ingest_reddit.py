import praw
import json
import os
from datetime import datetime, date

# Reddit API credentials from environment variables
client_id = os.getenv("REDDIT_CLIENT_ID")
client_secret = os.getenv("REDDIT_CLIENT_SECRET")
user_agent = os.getenv("REDDIT_USER_AGENT")

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
)

def fetch_comments_today(keywords, subreddits, limit=10, comment_limit=10):
    print(f"Searching for posts containing: {keywords}")
    results = []
    today_date = date.today()
    yesterday_date = today_date.replace(day=today_date.day - 3)

    for subreddit in subreddits:
        print(f"\nSearching in r/{subreddit}...")
        # Search for popular posts in the subreddit
        for submission in reddit.subreddit(subreddit).search(
            keywords, limit=limit, sort='top', time_filter='week'
        ):
            submission.comments.replace_more(limit=0)  # Flatten comment tree
            comments_list = list(submission.comments)  # Convert to list of comments
            comments_list.sort(key=lambda comment: comment.created_utc, reverse=True)  # Sort by newest comments
            
            for comment in comments_list[:comment_limit]:  # Limit number of comments per post
                try:
                    # Convert the comment's UTC timestamp to a date
                    comment_datetime = datetime.utcfromtimestamp(comment.created_utc)
                    comment_date = comment_datetime.date()

                    # Check if the comment was created today
                    if comment_date == yesterday_date:
                        print(f"Comment ID: {comment.id}, Created Date: {comment_date}")
                        results.append({
                            "id": comment.id,  # Unique comment ID
                            "body": comment.body,  # Comment text
                            "date": comment_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                            "submission_title": submission.title  # Title of the post the comment belongs to
                        })
                except Exception as e:
                    # Log any errors while parsing the comment
                    print(f"Error processing comment ID {comment.id if 'id' in dir(comment) else 'unknown'}: {e}")
    return results


if __name__ == "__main__":
    # Define keywords and target subreddits
    keywords = "Indo-Pacific OR China OR Taiwan"
    subreddits = ["worldnews", "news", "geopolitics", "china", "taiwan", "politics"]

    # Fetch comments from today
    comments = fetch_comments_today(keywords, subreddits, limit=10, comment_limit=30)

    # Save results to JSON file
    output_file = "reddit_comments.json"
    if comments:
        with open(output_file, "w") as file:
            json.dump(comments, file, indent=4)
        print(f"\nSearch complete! Results saved to {output_file}.")
    else:
        print(f"\nNo comments from today found. Check logs for more information.")
