def validate_ip(ip):
    try:
        parts = ip.split('.')
        
        if len(parts) != 4:
            return False
        
        for part in parts:
            num = int(part)
            if num < 0 or num > 255:
                return False
        
        return True
    
    except (ValueError, AttributeError):
        return False