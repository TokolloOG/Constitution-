def check_law_1(data):
    """
    Law 1: Verify required fields exist
    Required fields: "api_key", "user_id", "action"
    
    Args:
        data (dict): Request data to validate
        
    Returns:
        dict: {"valid": bool, "error": str or None, "law": 1, "message": str or None}
    """
    required_fields = ["api_key", "user_id", "action"]
    
    for field in required_fields:
        # Check if field is missing
        if field not in data:
            return {
                "valid": False,
                "error": "Missing required field: " + field,
                "law": 1
            }
        
        # Check if field is None or empty string
        if data[field] is None or (isinstance(data[field], str) and data[field].strip() == ""):
            return {
                "valid": False,
                "error": "Missing required field: " + field,
                "law": 1
            }
    
    # All required fields exist and have values
    return {
        "valid": True,
        "law": 1,
        "message": "Law 1 passed"
    }
