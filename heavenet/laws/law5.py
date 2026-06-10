from datetime import datetime

def check_law_5(data):
    """
    Law 5: Check if IP is 127.0.0.1 (localhost)
    
    Args:
        data (dict): Request data to validate
        
    Returns:
        dict: {"valid": bool, "law": 5, "ip": str, "timestamp": str}
    """
    ip = data.get("ip", "unknown")
    timestamp = datetime.now().isoformat()
    
    if ip == "127.0.0.1":
        return {
            "valid": True,
            "law": 5,
            "ip": ip,
            "timestamp": timestamp
        }
    else:
        return {
            "valid": False,
            "law": 5,
            "ip": ip,
            "timestamp": timestamp
        }
