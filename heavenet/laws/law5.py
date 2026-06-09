from datetime import datetime

def check(data):
    allowed = data.get('ip') == '127.0.0.1'
    
    return {
        "allowed": allowed,
        "ip": data.get('ip'),
        "timestamp": datetime.now().isoformat()
    }
