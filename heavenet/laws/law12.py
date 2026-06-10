def check_law_12(data):
    """
    Final security check: ensure no SQL injection keywords exist in any string value.
    Checks for dangerous SQL keywords: DROP, DELETE, UNION, INSERT, UPDATE, SELECT.
    
    Args:
        data (dict): Request data to validate
        
    Returns:
        dict: {"valid": bool, "error": str or None}
    """
    # SQL injection keywords to check for
    dangerous_keywords = ['DROP', 'DELETE', 'UNION', 'INSERT', 'UPDATE', 'SELECT']
    
    def check_for_sql_injection(obj, path="root"):
        """
        Recursively scans all string values in the data structure for SQL injection keywords.
        
        Args:
            obj: Object to scan
            path: Current path in the object for error reporting
            
        Returns:
            tuple: (is_safe, error_message)
        """
        # If it's a string, check for dangerous keywords
        if isinstance(obj, str):
            obj_upper = obj.upper()
            for keyword in dangerous_keywords:
                if keyword in obj_upper:
                    return False, f"SQL injection detected at {path}: found '{keyword}' keyword"
        
        # If it's a dictionary, recursively check all values
        elif isinstance(obj, dict):
            for key, value in obj.items():
                new_path = f"{path}.{key}"
                is_safe, error = check_for_sql_injection(value, new_path)
                if not is_safe:
                    return False, error
        
        # If it's a list, recursively check all items
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                new_path = f"{path}[{i}]"
                is_safe, error = check_for_sql_injection(item, new_path)
                if not is_safe:
                    return False, error
        
        return True, None
    
    try:
        if not isinstance(data, dict):
            return {"valid": False, "error": "Data must be a dictionary"}
        
        is_safe, error_msg = check_for_sql_injection(data)
        
        if not is_safe:
            return {"valid": False, "error": error_msg}
        
        return {"valid": True}
    
    except Exception as e:
        return {"valid": False, "error": f"SQL injection check error: {str(e)}"}
