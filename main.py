import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
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

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

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

@app.route('/verify', methods=['POST'])
def verify():
    """
    POST /verify endpoint
    Accepts JSON data and runs all 12 law checks in order.
    If any check fails, returns error with status 400.
    If all pass, returns success with status 200.
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if data is None:
            return jsonify({
                "status": "error",
                "message": "Invalid or missing JSON data"
            }), 400
        
        # Run all 12 laws in order
        results = []
        
        for index, law_check in enumerate(LAWS, start=1):
            try:
                result = law_check(data)
                results.append({
                    "law": index,
                    "result": result
                })
                
                # If any check fails, stop and return the error
                if not result.get("valid", False):
                    return jsonify({
                        "status": "rejected",
                        "failed_law": index,
                        "error": result.get("error", "Unknown error"),
                        "message": "Law " + str(index) + " validation failed"
                    }), 400
            
            except Exception as e:
                return jsonify({
                    "status": "error",
                    "failed_law": index,
                    "error": "Exception in Law " + str(index) + ": " + str(e),
                    "message": "Error processing law check"
                }), 400
        
        # All 12 laws passed
        return jsonify({
            "status": "approved",
            "message": "All 12 laws passed"
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e),
            "message": "Server error during verification"
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Heavenet API is running"
    }), 200

if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
