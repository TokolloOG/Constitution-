import hashlib

def check_law_11(data):
    """
    Law 11: Verifies 'checksum' field matches MD5 hash of concatenated data values.
    
    Args:
        data (dict): Request data containing a 'checksum' field and other data fields
        
    Returns:
        dict: {"valid": bool, "error": str or None}
    """
    if 'checksum' not in data:
        return {"valid": False, "error": "Missing checksum field", "law": 11}
    
    provided_checksum = data['checksum']
    
    try:
        # Get all values except the checksum field
        data_values = []
        for key in sorted(data.keys()):
            if key != 'checksum':
                value = data[key]
                # Convert value to string for concatenation
                data_values.append(str(value))
        
        # Concatenate all data values
        concatenated = ''.join(data_values)
        
        # Calculate MD5 hash of concatenated values
        calculated_checksum = hashlib.md5(concatenated.encode()).hexdigest()
        
        # Compare checksums
        if provided_checksum != calculated_checksum:
            return {
                "valid": False,
                "error": "Checksum mismatch. Expected: " + calculated_checksum + ", Got: " + provided_checksum,
                "law": 11
            }
        
        return {"valid": True, "law": 11}
    
    except Exception as e:
        return {"valid": False, "error": "Checksum verification error: " + str(e), "law": 11}
