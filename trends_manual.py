import json
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

MANUAL_TRENDS_FILE = 'data/manual_trends.json'

def get_manual_trends():
    """
    Fetch manually entered trends from the JSON file.
    
    Returns:
        list: A list of manually entered trends
    """
    try:
        # Create file if it doesn't exist
        if not os.path.exists(MANUAL_TRENDS_FILE):
            with open(MANUAL_TRENDS_FILE, 'w') as f:
                json.dump([], f)
        
        # Read existing trends
        with open(MANUAL_TRENDS_FILE, 'r') as f:
            trends = json.load(f)
        
        return trends
    
    except Exception as e:
        logger.error(f"Error reading manual trends: {str(e)}")
        return []

def add_manual_trend(trend_data):
    """
    Add a new manually entered trend to the JSON file.
    
    Args:
        trend_data (dict): The trend data to add
        
    Returns:
        bool: Success status
    """
    try:
        # Validate required fields
        required_fields = ['trend_name', 'source', 'category', 'lifecycle_stage']
        for field in required_fields:
            if field not in trend_data or not trend_data[field]:
                raise ValueError(f"Missing required field: {field}")
        
        # Read existing trends
        trends = get_manual_trends()
        
        # Add timestamp and UUID
        trend_data['timestamp'] = datetime.now().isoformat()
        
        # Add the new trend
        trends.append(trend_data)
        
        # Write back to file
        with open(MANUAL_TRENDS_FILE, 'w') as f:
            json.dump(trends, f, indent=2)
        
        return True
    
    except Exception as e:
        logger.error(f"Error adding manual trend: {str(e)}")
        raise
