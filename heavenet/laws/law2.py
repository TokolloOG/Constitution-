from datetime import datetime

def check_law_2(data):
    """
    Law 2: Verify API key is correct
    Expected: data["api_key"] == "heavenet-secret-123"
    
    Args:
        data (dict): Request data to validate
        
    Returns:
        dict: {"valid": bool, "law": 2, "ip": str, "timestamp": str}
    """
    api_key = data.get("api_key", "")
    ip = data.get("ip", "unknown")
    timestamp = datetime.now().isoformat()
    
    if api_key == "heavenet-secret-123":
        return {
            "valid": True,
            "law": 2,
            "ip": ip,
            "timestamp": timestamp
        }
    else:
        return {
            "valid": False,
            "law": 2,
            "ip": ip,
            "timestamp": timestamp
        }
