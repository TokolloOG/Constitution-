import ipaddress

def check_law_7(data):
    """
    Law 7: Validates if 'ip' address is not in the blocked list.
    
    Args:
        data (dict): Request data to validate
        
    Returns:
        dict: {"valid": bool, "error": str or None}
    """
    blocked_ips = ['192.168.0.1', '10.0.0.1']
    
    if 'ip' not in data:
        return {"valid": False, "error": "Missing ip", "law": 7}
    
    ip_str = data['ip']
    
    try:
        # Validate and parse the IP address
        ip_obj = ipaddress.ip_address(ip_str)
        
        # Check if IP is in blocked list
        if str(ip_obj) in blocked_ips:
            return {"valid": False, "error": "IP address " + ip_str + " is blocked", "law": 7}
        
        return {"valid": True, "law": 7}
    
    except ValueError:
        return {"valid": False, "error": "Invalid IP address: " + ip_str, "law": 7}
