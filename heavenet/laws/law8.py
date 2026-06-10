from datetime import datetime, timedelta
from collections import defaultdict

# In-memory dictionary to track requests per user_id
# Format: {user_id: [(timestamp1, timestamp2, ...), ...]}
request_tracker = defaultdict(list)

# Rate limit: 100 requests per minute per user
RATE_LIMIT = 100
WINDOW_SECONDS = 60

def check_law_8(data):
    """
    Law 8: Validates rate limit: max 100 requests per user_id per minute.
    Uses in-memory tracking with timestamp windows.
    
    Args:
        data (dict): Request data containing 'user_id'
        
    Returns:
        dict: {"valid": bool, "error": str or None, "requests_remaining": int or None}
    """
    if 'user_id' not in data:
        return {"valid": False, "error": "Missing user_id", "law": 8}
    
    user_id = data['user_id']
    current_time = datetime.now()
    window_start = current_time - timedelta(seconds=WINDOW_SECONDS)
    
    try:
        # Clean up old timestamps (older than 1 minute)
        request_tracker[user_id] = [
            ts for ts in request_tracker[user_id] 
            if ts > window_start
        ]
        
        # Get current request count in the window
        current_requests = len(request_tracker[user_id])
        
        # Check if rate limit exceeded
        if current_requests >= RATE_LIMIT:
            requests_remaining = 0
            return {
                "valid": False,
                "error": "Rate limit exceeded: " + str(current_requests) + "/" + str(RATE_LIMIT) + " requests in the last minute",
                "requests_remaining": requests_remaining,
                "law": 8
            }
        
        # Add current request timestamp
        request_tracker[user_id].append(current_time)
        
        # Calculate remaining requests
        requests_remaining = RATE_LIMIT - len(request_tracker[user_id])
        
        return {
            "valid": True,
            "requests_remaining": requests_remaining,
            "law": 8
        }
    
    except Exception as e:
        return {"valid": False, "error": "Rate limit check error: " + str(e), "law": 8}
