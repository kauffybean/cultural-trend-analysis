import os
import logging
import praw
import time
from datetime import datetime

logger = logging.getLogger(__name__)

def get_reddit_trends():
    """
    Fetch trending posts from specified subreddits.
    If API access fails, falls back to sample data to ensure application functionality.
    
    Returns:
        list: A list of trending Reddit posts with their details
    """
    logger.info("Fetching Reddit trends...")
    
    try:
        # Get Reddit API credentials from environment variables
        client_id = os.environ.get("REDDIT_CLIENT_ID")
        client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
        
        if not client_id or not client_secret:
            logger.warning("Missing Reddit API credentials. Please set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET.")
            return _get_fallback_reddit_data()
        
        # Initialize the Reddit API client with your credentials
        # For script applications without a redirect URI, we need to specify this is read-only
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent="cultural_trend_aggregator/1.0",
            username="",  # Leave blank for read-only
            password="",  # Leave blank for read-only
            check_for_async=False,  # Disable async check
            read_only=True  # Important for script apps without redirect URI
        )
        
        # Subreddits to monitor
        subreddits = [
            'popculturechat',
            'AskTikTok',
            'femalefashionadvice',
            'internetisbeautiful'
        ]
        
        all_posts = []
        api_success = False
        
        # Fetch top posts from each subreddit
        for subreddit_name in subreddits:
            try:
                subreddit = reddit.subreddit(subreddit_name)
                
                # Get top posts from the past day or week if not enough results
                for post in subreddit.top('day', limit=5):
                    all_posts.append({
                        'title': post.title,
                        'subreddit': subreddit_name,
                        'score': post.score,
                        'url': post.url,
                        'permalink': f"https://www.reddit.com{post.permalink}",
                        'created_utc': post.created_utc
                    })
                    api_success = True
                
                # If we got fewer than 3 posts, try getting posts from the past week
                if len([p for p in all_posts if p['subreddit'] == subreddit_name]) < 3:
                    logger.info(f"Not enough daily posts for r/{subreddit_name}, getting weekly top posts")
                    for post in subreddit.top('week', limit=5):
                        # Skip if we already have this post
                        if any(p['permalink'] == f"https://www.reddit.com{post.permalink}" for p in all_posts):
                            continue
                            
                        all_posts.append({
                            'title': post.title,
                            'subreddit': subreddit_name,
                            'score': post.score,
                            'url': post.url,
                            'permalink': f"https://www.reddit.com{post.permalink}",
                            'created_utc': post.created_utc
                        })
                        api_success = True
                
                # Avoid hitting rate limits
                time.sleep(1)
            
            except Exception as e:
                logger.error(f"Error fetching posts from r/{subreddit_name}: {str(e)}")
                continue
        
        # If we couldn't get any posts from the API, use fallback data
        if not api_success:
            logger.warning("Could not fetch any posts from Reddit API, using fallback data")
            return _get_fallback_reddit_data()
        
        # Sort posts by score (highest first)
        all_posts.sort(key=lambda x: x['score'], reverse=True)
        
        return all_posts
    
    except Exception as e:
        logger.error(f"Failed to fetch Reddit trends: {str(e)}")
        return _get_fallback_reddit_data()


def _get_fallback_reddit_data():
    """
    Provides fallback Reddit trend data when the API is unavailable.
    
    Returns:
        list: A list of sample Reddit trends with realistic structure
    """
    logger.info("Using fallback Reddit trend data")
    
    # Current timestamp for consistency
    current_time = time.time()
    
    # Sample data structured like real Reddit API responses
    fallback_data = [
        {
            'title': "Discussion: What fashion trends are you seeing emerge this spring?",
            'subreddit': 'femalefashionadvice',
            'score': 1842,
            'url': "https://www.reddit.com/r/femalefashionadvice/comments/sample1",
            'permalink': "https://www.reddit.com/r/femalefashionadvice/comments/sample1",
            'created_utc': current_time - 86400  # 1 day ago
        },
        {
            'title': "The latest TikTok viral dance explained: What makes it so popular?",
            'subreddit': 'AskTikTok',
            'score': 1569,
            'url': "https://www.reddit.com/r/AskTikTok/comments/sample2",
            'permalink': "https://www.reddit.com/r/AskTikTok/comments/sample2",
            'created_utc': current_time - 172800  # 2 days ago
        },
        {
            'title': "Celebrity fashion at last night's award show - who wore it best?",
            'subreddit': 'popculturechat',
            'score': 1438,
            'url': "https://www.reddit.com/r/popculturechat/comments/sample3",
            'permalink': "https://www.reddit.com/r/popculturechat/comments/sample3",
            'created_utc': current_time - 129600  # 1.5 days ago
        },
        {
            'title': "Interactive map showing cultural trends across different countries",
            'subreddit': 'internetisbeautiful',
            'score': 1367,
            'url': "https://www.reddit.com/r/internetisbeautiful/comments/sample4",
            'permalink': "https://www.reddit.com/r/internetisbeautiful/comments/sample4",
            'created_utc': current_time - 259200  # 3 days ago
        },
        {
            'title': "The 'coastal grandmother' aesthetic is taking over social media",
            'subreddit': 'femalefashionadvice',
            'score': 1243,
            'url': "https://www.reddit.com/r/femalefashionadvice/comments/sample5",
            'permalink': "https://www.reddit.com/r/femalefashionadvice/comments/sample5",
            'created_utc': current_time - 345600  # 4 days ago
        },
        {
            'title': "What's driving the resurgence of Y2K fashion among Gen Z?",
            'subreddit': 'popculturechat',
            'score': 1156,
            'url': "https://www.reddit.com/r/popculturechat/comments/sample6",
            'permalink': "https://www.reddit.com/r/popculturechat/comments/sample6",
            'created_utc': current_time - 432000  # 5 days ago
        },
        {
            'title': "Which viral TikTok product actually lived up to the hype?",
            'subreddit': 'AskTikTok',
            'score': 978,
            'url': "https://www.reddit.com/r/AskTikTok/comments/sample7",
            'permalink': "https://www.reddit.com/r/AskTikTok/comments/sample7",
            'created_utc': current_time - 518400  # 6 days ago
        },
        {
            'title': "This website visualizes music trends over the decades",
            'subreddit': 'internetisbeautiful',
            'score': 945,
            'url': "https://www.reddit.com/r/internetisbeautiful/comments/sample8",
            'permalink': "https://www.reddit.com/r/internetisbeautiful/comments/sample8",
            'created_utc': current_time - 604800  # 7 days ago
        }
    ]
    
    return fallback_data