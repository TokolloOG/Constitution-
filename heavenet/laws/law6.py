def check_law_6(data):
    """
    Validates if 'action' is one of the allowed actions: create, read, update, delete.
    
    Args:
        data (dict): Request data to validate
        
    Returns:
        dict: {"valid": bool, "error": str or None}
    """
    allowed_actions = ['create', 'read', 'update', 'delete']
    
    if 'action' not in data:
        return {"valid": False, "error": "Missing action"}
    
    action = data['action']
    
    if action not in allowed_actions:
        return {"valid": False, "error": "Invalid action"}
    
    return {"valid": True}
