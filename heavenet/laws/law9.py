def check_law_9(data):
    """
    Law 9: Validates JSON structure:
    - All keys must be strings
    - No nested objects deeper than 2 levels
    
    Args:
        data (dict): Request data to validate
        
    Returns:
        dict: {"valid": bool, "error": str or None}
    """
    
    def validate_structure(obj, depth=0, path="root"):
        """
        Recursively validates the structure of the object.
        
        Args:
            obj: Object to validate
            depth: Current depth level (0 = root)
            path: Current path in the object for error reporting
            
        Returns:
            tuple: (is_valid, error_message)
        """
        # Check if we've exceeded max depth (2 levels deep means depth 2)
        if depth > 2:
            return False, "Nesting too deep at " + path + " (max 2 levels allowed)"
        
        # If it's a dictionary, validate all keys and values
        if isinstance(obj, dict):
            for key, value in obj.items():
                # Check if key is a string
                if not isinstance(key, str):
                    return False, "Key at " + path + " is not a string: " + type(key).__name__
                
                # Recursively validate the value
                new_path = path + "." + key
                is_valid, error = validate_structure(value, depth + 1, new_path)
                if not is_valid:
                    return False, error
        
        # If it's a list, validate each element
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                new_path = path + "[" + str(i) + "]"
                is_valid, error = validate_structure(item, depth + 1, new_path)
                if not is_valid:
                    return False, error
        
        # Primitive types are valid
        return True, None
    
    try:
        if not isinstance(data, dict):
            return {"valid": False, "error": "Root data must be a dictionary", "law": 9}
        
        is_valid, error_msg = validate_structure(data, depth=0)
        
        if not is_valid:
            return {"valid": False, "error": error_msg, "law": 9}
        
        return {"valid": True, "law": 9}
    
    except Exception as e:
        return {"valid": False, "error": "JSON structure validation error: " + str(e), "law": 9}
