from datetime import datetime

def check(data):
    allowed = data.get('api_key') == 'heavenet-secret-123'
    
    return {
        "allowed": allowed,
        "ip": data.get('ip'),
        "timestamp": datetime.now().isoformat()
    }
