import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def check_law_2(data):
    """
    Law 2: Verify API key is correct
    Expected: data["api_key"] == os.getenv("HEAVENET_API_KEY")
    
    Args:
        data (dict): Request data to validate
        
    Returns:
        dict: {"valid": bool, "law": 2, "ip": str, "timestamp": str}
    """
    api_key = data.get("api_key", "")
    ip = data.get("ip", "unknown")
    timestamp = datetime.now().isoformat()
    
    expected_api_key = os.getenv("HEAVENET_API_KEY")
    
    if api_key == expected_api_key:
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
