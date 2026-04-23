import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.security_scanner import SecurityScanner

class TestSecurityScanner:
    
    def test_dangerous_function_detection(self):
        """Test detection of dangerous functions"""
        code = """
result = eval(user_input)
os.system("rm -rf /")
exec("print('hello')")
"""
        scanner = SecurityScanner()
        result = scanner.scan(code)
        
        assert 'high_risk' in result
        assert len(result['high_risk']) > 0
    
    def test_hardcoded_secret_detection(self):
        """Test detection of hardcoded secrets"""
        code = """
password = "admin123"
API_KEY = "sk-1234567890"
secret_token = "mysecret"
"""
        scanner = SecurityScanner()
        result = scanner.scan(code)
        
        assert 'medium_risk' in result
        # Should detect at least one hardcoded secret
    
    def test_sql_injection_detection(self):
        """Test SQL injection pattern detection"""
        code = """
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)
"""
        scanner = SecurityScanner()
        result = scanner.scan(code)
        
        assert 'medium_risk' in result or 'high_risk' in result
    
    def test_secure_code_no_warnings(self):
        """Test secure code doesn't trigger warnings"""
        code = """
def add(a, b):
    return a + b

def greet(name):
    print(f"Hello {name}")
"""
        scanner = SecurityScanner()
        result = scanner.scan(code)
        
        # Security score should be high
        assert result.get('security_score', 0) >= 80
    
    def test_network_operations_detection(self):
        """Test detection of network operations"""
        code = """
import requests
response = requests.get("https://api.example.com/data")
"""
        scanner = SecurityScanner()
        result = scanner.scan(code)
        
        assert 'low_risk' in result or 'medium_risk' in result