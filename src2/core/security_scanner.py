# core/security_scanner.py
"""
Security pattern detection in code
"""

import ast
import re
from typing import List, Dict, Any

class SecurityScanner:
    """
    Detect security-relevant patterns in code:
    - Dangerous function calls
    - Network operations
    - File I/O
    - Cryptography usage
    - Potential vulnerabilities
    """
    
    def __init__(self):
        self.patterns = {
            'dangerous_functions': [
                'eval', 'exec', '__import__', 'compile',
                'open', 'os.system', 'subprocess.Popen',
                'pickle.loads', 'yaml.load'
            ],
            'network_indicators': [
                'requests.get', 'requests.post', 'urllib.request',
                'socket.socket', 'http.client', 'websocket'
            ],
            'file_operations': [
                'open', 'file.read', 'file.write', 'os.remove',
                'shutil.rmtree', 'os.unlink'
            ],
            'crypto_indicators': [
                'hashlib', 'cryptography', 'secrets', 'hmac',
                'rsa', 'aes', 'fernet'
            ],
            'sql_injection_risk': [
                'execute', 'executemany', 'raw_input'
            ],
            'hardcoded_secrets': [
                'password', 'secret', 'key', 'token', 'api_key'
            ]
        }
        
        self.severity_levels = {
            'high': ['eval', 'exec', 'os.system', 'subprocess'],
            'medium': ['open', 'pickle', 'yaml'],
            'low': ['requests', 'socket']
        }
    
    def scan(self, source_code: str, ast_data: Dict = None) -> Dict[str, Any]:
        """
        Scan code for security issues
        """
        findings = {
            'high_risk': [],
            'medium_risk': [],
            'low_risk': [],
            'security_score': 100,  # Start with perfect score
            'recommendations': []
        }
        
        # Scan for dangerous functions
        dangerous = self._find_dangerous_functions(source_code)
        findings.update(dangerous)
        
        # Scan for hardcoded secrets
        secrets = self._find_hardcoded_secrets(source_code)
        if secrets:
            findings['medium_risk'].extend(secrets)
            findings['security_score'] -= len(secrets) * 5
        
        # Check for network operations
        network = self._find_network_operations(source_code)
        if network:
            findings['low_risk'].extend(network)
            findings['security_score'] -= len(network) * 2
        
        # Check file operations
        file_ops = self._find_file_operations(source_code)
        if file_ops:
            findings['medium_risk'].extend(file_ops)
            findings['security_score'] -= len(file_ops) * 3
        
        # Generate recommendations
        findings['recommendations'] = self._generate_recommendations(findings)
        
        # Ensure score is within 0-100
        findings['security_score'] = max(0, min(100, findings['security_score']))
        
        return findings
    
    def _find_dangerous_functions(self, code: str) -> Dict:
        """Find dangerous function calls"""
        high_risk = []
        medium_risk = []
        
        for pattern in self.patterns['dangerous_functions']:
            if pattern in code:
                if any(high in pattern for high in self.severity_levels['high']):
                    high_risk.append(pattern)
                else:
                    medium_risk.append(pattern)
        
        return {
            'high_risk': high_risk,
            'medium_risk': medium_risk
        }
    
    def _find_hardcoded_secrets(self, code: str) -> List[str]:
        """Find potential hardcoded secrets"""
        secrets = []
        
        # Check for variable assignments with secret-related names
        lines = code.split('\n')
        for i, line in enumerate(lines):
            line_lower = line.lower()
            for pattern in self.patterns['hardcoded_secrets']:
                if pattern in line_lower and ('=' in line or '=' in line_lower):
                    # Check if it's likely a hardcoded value
                    if any(quote in line for quote in ['"', "'"]):
                        secrets.append(f"Line {i+1}: Potential hardcoded {pattern}")
        
        return secrets
    
    def _find_network_operations(self, code: str) -> List[str]:
        """Find network-related operations"""
        network_ops = []
        
        for pattern in self.patterns['network_indicators']:
            if pattern in code:
                network_ops.append(pattern)
        
        return network_ops
    
    def _find_file_operations(self, code: str) -> List[str]:
        """Find file operations - avoid false positives"""
        file_ops = []
        
        # Match only actual function calls, not substrings
        import re
        patterns = ['open\(', 'file\.read\(', 'file\.write\(', 'os\.remove\(']
        
        for pattern in patterns:
            if re.search(pattern, code):
                # Extract just the function name without parentheses
                func_name = pattern.replace('\(', '')
                file_ops.append(func_name)
        
        return list(set(file_ops))  # Remove duplicates
    
    def _generate_recommendations(self, findings: Dict) -> List[str]:
        """Generate security recommendations"""
        recommendations = []
        
        if findings['high_risk']:
            recommendations.append(
                f"⚠️ High-risk functions detected: {', '.join(findings['high_risk'])}. "
                "Consider using safer alternatives or adding input validation."
            )
        
        if findings['medium_risk']:
            recommendations.append(
                f"Medium-risk operations found: {', '.join(findings['medium_risk'][:3])}. "
                "Ensure proper error handling and access controls."
            )
        
        if findings.get('hardcoded_secrets'):
            recommendations.append(
                "Hardcoded secrets detected. Use environment variables or secure vaults instead."
            )
        
        if findings['security_score'] < 70:
            recommendations.append(
                "Security score is low. Review code for vulnerabilities and implement security best practices."
            )
        
        return recommendations