cd ~/heavenet
cat > main.py << 'EOF'
from laws import law1, law2, law3, law4, law5, law6, law7, law8, law9, law10, law11, law12

LAWS = [law1, law2, law3, law4, law5, law6, law7, law8, law9, law10, law11, law12]

def run_all_laws(data):
    """Run data through all 12 laws in order"""
    results = []
    for law in LAWS:
        result = law.check(data)
        results.append(result)
        if not result["allowed"]:
            return {"blocked_by": result["law"], "results": results}
    return {"blocked_by": None, "results": results}

if __name__ == "__main__":
    # Test data
    test_data = {
        "api_key": "heavenet-secret-123",
        "ip": "127.0.0.1"
    }
    
    output = run_all_laws(test_data)
    print(output)
EOF