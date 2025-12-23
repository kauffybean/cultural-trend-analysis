import json
import os
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

CACHE_FILE = 'data/trend_cache.json'
CACHE_DURATION_MINUTES = 15

def get_cached_trends():
    """
    Get trends from cache if available and not expired.
    
    Returns:
        list or None: Cached trends if valid, None otherwise
    """
    try:
        if not os.path.exists(CACHE_FILE):
            return None
            
        with open(CACHE_FILE, 'r') as f:
            cache_data = json.load(f)
        
        cache_time = datetime.fromisoformat(cache_data.get('timestamp', '2000-01-01'))
        if datetime.utcnow() - cache_time > timedelta(minutes=CACHE_DURATION_MINUTES):
            logger.info("Cache expired")
            return None
            
        return cache_data.get('trends', [])
        
    except Exception as e:
        logger.error(f"Error reading cache: {str(e)}")
        return None

def set_cached_trends(trends):
    """
    Save trends to cache with timestamp.
    
    Args:
        trends (list): The trends to cache
    """
    try:
        os.makedirs('data', exist_ok=True)
        cache_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'trends': trends
        }
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache_data, f)
        logger.info(f"Cached {len(trends)} trends")
    except Exception as e:
        logger.error(f"Error writing cache: {str(e)}")

def get_cache_status():
    """
    Get information about the current cache status.
    
    Returns:
        dict: Cache status information
    """
    try:
        if not os.path.exists(CACHE_FILE):
            return {'exists': False, 'count': 0, 'age_minutes': None}
            
        with open(CACHE_FILE, 'r') as f:
            cache_data = json.load(f)
        
        cache_time = datetime.fromisoformat(cache_data.get('timestamp', '2000-01-01'))
        age = datetime.utcnow() - cache_time
        
        return {
            'exists': True,
            'count': len(cache_data.get('trends', [])),
            'age_minutes': int(age.total_seconds() / 60),
            'timestamp': cache_data.get('timestamp')
        }
    except Exception as e:
        logger.error(f"Error getting cache status: {str(e)}")
        return {'exists': False, 'count': 0, 'age_minutes': None, 'error': str(e)}
