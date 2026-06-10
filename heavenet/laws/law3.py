def check_law_3(data):
    """
    Law 3: Check if user_id is a positive integer
    
    Args:
        data (dict): Request data to validate
        
    Returns:
        dict: {"valid": bool, "law": 3}
    """
    user_id = data.get("user_id")
    
    # Check if user_id is an integer and positive
    if isinstance(user_id, int) and user_id > 0:
        return {
            "valid": True,
            "law": 3
        }
    else:
        return {
            "valid": False,
            "law": 3
        }
