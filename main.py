from heavenet.laws.law1 import check_law_1
from heavenet.laws.law2 import check_law_2
from heavenet.laws.law3 import check_law_3
from heavenet.laws.law4 import check_law_4
from heavenet.laws.law5 import check_law_5
from heavenet.laws.law6 import check_law_6
from heavenet.laws.law7 import check_law_7
from heavenet.laws.law8 import check_law_8
from heavenet.laws.law9 import check_law_9
from heavenet.laws.law10 import check_law_10
from heavenet.laws.law11 import check_law_11
from heavenet.laws.law12 import check_law_12

# List of all law check functions in order
LAWS = [
    check_law_1,
    check_law_2,
    check_law_3,
    check_law_4,
    check_law_5,
    check_law_6,
    check_law_7,
    check_law_8,
    check_law_9,
    check_law_10,
    check_law_11,
    check_law_12
]

def run_all_laws(data):
    """
    Run data through all 12 laws in order.
    If any check returns valid=False, stop and return that error.
    Only return success if all 12 pass.
    
    Args:
        data (dict): Request data to validate
        
    Returns:
        dict: Success or error response with law results
    """
    results = []
    
    for index, law_check in enumerate(LAWS, start=1):
        result = law_check(data)
        results.append({
            "law": index,
            "result": result
        })
        
        # If any check fails, stop and return the error
        if not result.get("valid", False):
            return {
                "success": False,
                "failed_law": index,
                "error": result.get("error", "Unknown error"),
                "results": results
            }
    
    # All 12 laws passed
    return {
        "success": True,
        "message": "All 12 laws passed successfully",
        "results": results
    }

if __name__ == "__main__":
    # Test data
    test_data = {
        "api_key": "heavenet-secret-123",
        "ip": "127.0.0.1",
        "user_id": "user123",
        "action": "read",
        "user_agent": "Mozilla/5.0",
        "timestamp": 1623456789,
        "data_field": "test_value"
    }
    
    output = run_all_laws(test_data)
    print(output)
