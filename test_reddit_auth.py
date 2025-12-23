import os
import praw
import sys

def test_reddit_auth():
    # Get environment variables
    client_id = os.environ.get("REDDIT_CLIENT_ID")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
    
    print(f"Client ID available: {client_id is not None}")
    print(f"Client Secret available: {client_secret is not None}")
    
    # If credentials are missing, exit
    if not client_id or not client_secret:
        print("Error: Missing Reddit API credentials")
        return False
    
    try:
        # Initialize the Reddit API client with the same settings as in our app
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent="cultural_trend_aggregator_test/1.0",
            username="",  # Leave blank for read-only
            password="",  # Leave blank for read-only
            check_for_async=False,  # Disable async check
            read_only=True  # Important for script apps without redirect URI
        )
        
        # Test if we can access Reddit
        # This will fail if auth isn't working
        subreddit = reddit.subreddit("all")
        for post in subreddit.hot(limit=1):
            print(f"Successfully accessed Reddit. Post title: {post.title}")
            return True
    
    except Exception as e:
        print(f"Error testing Reddit API: {str(e)}")
        return False
        
if __name__ == "__main__":
    if test_reddit_auth():
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Error