import os
import logging
import datetime
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

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
    Logs all requests and failures.
    If any checks fail, returns error with status 400 and list of failed laws.
    If all pass, returns success with status 200.
    """
    try:
        # Log incoming request
        logger.info("Request received from IP: {}".format(request.remote_addr))
        
        # Get JSON data from request
        data = request.get_json()
        
        if data is None:
            logger.warning("Invalid or missing JSON data")
            return jsonify({
                "status": "error",
                "message": "Invalid or missing JSON data",
                "timestamp": datetime.datetime.now().isoformat()
            }), 400
        
        # Run all 12 laws in order
        failed_laws = []
        
        for index, law_check in enumerate(LAWS, start=1):
            try:
                result = law_check(data)
                
                # If any check fails, add to failed_laws list
                if not result.get("valid", False):
                    failed_laws.append(index)
                    logger.warning("Law {} failed".format(index))
            
            except Exception as e:
                failed_laws.append(index)
                logger.warning("Law {} failed with exception: {}".format(index, str(e)))
        
        # If any laws failed, return rejection
        if failed_laws:
            logger.warning("Request rejected due to failed laws: {}".format(failed_laws))
            return jsonify({
                "status": "rejected",
                "failed_laws": failed_laws,
                "timestamp": datetime.datetime.now().isoformat()
            }), 400
        
        # All 12 laws passed
        logger.info("All 12 laws passed")
        return jsonify({
            "status": "approved",
            "message": "All 12 laws passed",
            "timestamp": datetime.datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        logger.error("Server error during verification: {}".format(str(e)))
        return jsonify({
            "status": "error",
            "error": str(e),
            "message": "Server error during verification",
            "timestamp": datetime.datetime.now().isoformat()
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    logger.info("Health check request")
    return jsonify({
        "status": "healthy",
        "message": "Heavenet API is running",
        "timestamp": datetime.datetime.now().isoformat()
    }), 200

if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    logger.info("Starting Heavenet API on port {}".format(port))
    app.run(debug=True, host='0.0.0.0', port=port)
