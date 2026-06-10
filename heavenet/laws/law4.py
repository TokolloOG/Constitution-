from datetime import datetime, timedelta

def check_law_4(data):
    """
    Law 4: Check if timestamp is not older than 5 minutes
    
    Args:
        data (dict): Request data to validate
        
    Returns:
        dict: {"valid": bool, "law": 4}
    """
    timestamp = data.get("timestamp")
    
    if timestamp is None:
        return {
            "valid": False,
            "law": 4
        }
    
    try:
        # Convert timestamp to datetime if it's a Unix timestamp
        if isinstance(timestamp, (int, float)):
            request_time = datetime.fromtimestamp(timestamp)
        else:
            return {
                "valid": False,
                "law": 4
            }
        
        # Get current time and check if timestamp is within 5 minutes
        current_time = datetime.now()
        five_minutes_ago = current_time - timedelta(minutes=5)
        
        if request_time >= five_minutes_ago:
            return {
                "valid": True,
                "law": 4
            }
        else:
            return {
                "valid": False,
                "law": 4
            }
    except Exception:
        return {
            "valid": False,
            "law": 4
        }
