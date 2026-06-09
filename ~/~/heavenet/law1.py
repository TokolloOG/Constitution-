def check(data):
    """
    Law 1: Verify required fields exist
    Returns True if passed, False if blocked
    """
    required_fields = ["api_key", "user_id", "action"]

    for field in required_fields:
        if field not in data or data[field] is None or data[field] == "":
            return {
                "passed": False,
                "law": 1,
                "reason": f"Missing required field: {field}"
            }

    return {
        "passed": True,
        "law": 1,
        "reason": "All required fields present"
    }