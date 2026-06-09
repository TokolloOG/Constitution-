def check(data):
    required_fields = ['api_key', 'user_id', 'action']
    
    for field in required_fields:
        if field not in data or data[field] is None:
            return {"allowed": False}
    
    return {"allowed": True, "law": 1}
