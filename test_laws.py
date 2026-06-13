import requests
import json
from datetime import datetime

# API endpoint
API_URL = "http://localhost:5000/verify"

def print_test_header(test_num, test_name):
    """Print test header"""
    print("\n" + "="*60)
    print(f"TEST {test_num}: {test_name}")
    print("="*60)

def print_result(response_data, status_code):
    """Print response result"""
    print(f"Status Code: {status_code}")
    print(f"Response: {json.dumps(response_data, indent=2)}")
def test_verify_script_exists():
    """Law III: verify.js must exist to enforce Law I on hardware."""
    assert Path("verify.js").exists(), "Law I cannot be verified. verify.js missing."
def test_1_valid_data():
    """Test 1: Send valid data with correct api_key, user_id, action, ip=127.0.0.1"""
    print_test_header(1, "Valid Data - Should Pass All Laws")
    
    test_data = {
        "api_key": "heavenet-secret-123",
        "user_id": 12345,
        "action": "read",
        "ip": "127.0.0.1",
        "user_agent": "Mozilla/5.0",
        "timestamp": int(datetime.now().timestamp())
    }
    
    print(f"Request Data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(API_URL, json=test_data)
        print_result(response.json(), response.status_code)
        
        if response.status_code == 200:
            print("✓ PASSED: All laws validated successfully")
        else:
            print("✗ FAILED: Expected status 200 but got " + str(response.status_code))
    
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")

def test_2_missing_api_key():
    """Test 2: Send missing api_key → should fail on law1"""
    print_test_header(2, "Missing API Key - Should Fail on Law 1")
    
    test_data = {
        "user_id": 12345,
        "action": "read",
        "ip": "127.0.0.1",
        "user_agent": "Mozilla/5.0",
        "timestamp": int(datetime.now().timestamp())
    }
    
    print(f"Request Data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(API_URL, json=test_data)
        print_result(response.json(), response.status_code)
        
        if response.status_code == 400 and response.json().get("failed_law") == 1:
            print("✓ PASSED: Correctly failed on Law 1")
        else:
            print("✗ FAILED: Expected to fail on Law 1")
    
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")

def test_3_wrong_api_key():
    """Test 3: Send wrong api_key → should fail on law2"""
    print_test_header(3, "Wrong API Key - Should Fail on Law 2")
    
    test_data = {
        "api_key": "wrong-secret-key",
        "user_id": 12345,
        "action": "read",
        "ip": "127.0.0.1",
        "user_agent": "Mozilla/5.0",
        "timestamp": int(datetime.now().timestamp())
    }
    
    print(f"Request Data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(API_URL, json=test_data)
        print_result(response.json(), response.status_code)
        
        if response.status_code == 400 and response.json().get("failed_law") == 2:
            print("✓ PASSED: Correctly failed on Law 2")
        else:
            print("✗ FAILED: Expected to fail on Law 2")
    
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")

def test_4_wrong_ip():
    """Test 4: Send wrong ip → should fail on law5"""
    print_test_header(4, "Wrong IP Address - Should Fail on Law 5")
    
    test_data = {
        "api_key": "heavenet-secret-123",
        "user_id": 12345,
        "action": "read",
        "ip": "192.168.1.1",
        "user_agent": "Mozilla/5.0",
        "timestamp": int(datetime.now().timestamp())
    }
    
    print(f"Request Data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(API_URL, json=test_data)
        print_result(response.json(), response.status_code)
        
        if response.status_code == 400 and response.json().get("failed_law") == 5:
            print("✓ PASSED: Correctly failed on Law 5")
        else:
            print("✗ FAILED: Expected to fail on Law 5")
    
    except Exception as e:
        print(f"✗ ERROR: {str(e)}")

def main():
    """Run all tests"""
    print("\n" + "#"*60)
    print("# HEAVENET API - LAW VALIDATION TESTS")
    print("#"*60)
    print("\nStarting test suite...")
    print(f"API Endpoint: {API_URL}")
    
    try:
        # Run all tests
        test_1_valid_data()
        test_2_missing_api_key()
        test_3_wrong_api_key()
        test_4_wrong_ip()
        
        print("\n" + "#"*60)
        print("# TEST SUITE COMPLETED")
        print("#"*60 + "\n")
    
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Could not connect to API at " + API_URL)
        print("Make sure the Flask app is running: python main.py")
    
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")

if __name__ == "__main__":
    main()
import pytest
import yaml
from pathlib import Path

SCHEMATIC_PATH = Path("hardware/helios-one.kicad_sch")
BOM_PATH = Path("hardware/bom.yaml")

def test_law_i_mosfet_killswitch_exists():
    """
    Law I: Kill Switch is Physics
    Helios One MUST have a physical MOSFET that cuts power to ALL radios.
    Green LED off = <1mV at antenna. No software backdoor possible.
    """
    assert SCHEMATIC_PATH.exists(), "Helios One schematic missing. Law III violation."
    
    schematic = SCHEMATIC_PATH.read_text()
    assert "MOSFET_RF_CUT" in schematic, "Law I violation: No RF kill switch MOSFET found in schematic"
    assert "LED_POWER_RF" in schematic, "Law I violation: No physical LED indicator for radio power"
    
    # BOM must list the specific kill switch part
    bom = yaml.safe_load(BOM_PATH.read_text())
    killswitch_parts = [p for p in bom['parts'] if 'kill_switch' in p.get('tags', [])]
    assert len(killswitch_parts) >= 3, "Law I violation: Must have kill switches for WiFi, BT, Cellular"
    
    for part in killswitch_parts:
        assert part['type'] == 'MOSFET', f"Law I violation: {part['name']} must be hardware MOSFET, not GPIO"
        assert part['controlled_by'] == 'physical_switch', "Law I violation: Cannot be software controlled"

def test_law_ii_rep_not_equity():
    """
    Law II: Rep > Equity
    Repo must have no cap table, no SAFEs, no equity docs.
    """
    forbidden = ['cap_table', 'SAFE_', 'shareholder', 'investor_agreement']
    repo_files = list(Path(".").rglob("*"))
    for f in repo_files:
        assert not any(bad in f.name.lower() for bad in forbidden), f"Law II violation: {f} mentions equity"

if __name__ == "__main__":
    pytest.main([__file__])