def check_law_2(data):
    """
    Validates if the request contains 'api_key'.
    
    Args:
        data (dict): Request data to validate
        
    Returns:
        dict: {"valid": bool, "error": str or None}
    """
    if 'api_key' not in data or data['api_key'] is None:
        return {"valid": False, "error": "Missing api_key"}
    
    return {"valid": True}
