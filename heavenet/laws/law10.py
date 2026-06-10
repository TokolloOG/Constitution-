def check_law_10(data):
    """
    Law 10: Validates if 'user_agent' header exists and is not empty.
    
    Args:
        data (dict): Request data to validate
        
    Returns:
        dict: {"valid": bool, "error": str or None}
    """
    if 'user_agent' not in data:
        return {"valid": False, "error": "Missing user_agent", "law": 10}
    
    user_agent = data['user_agent']
    
    # Check if user_agent is None or empty string
    if user_agent is None or (isinstance(user_agent, str) and user_agent.strip() == ""):
        return {"valid": False, "error": "user_agent cannot be empty", "law": 10}
    
    # Ensure user_agent is a string
    if not isinstance(user_agent, str):
        return {"valid": False, "error": "user_agent must be a string", "law": 10}
    
    return {"valid": True, "law": 10}
