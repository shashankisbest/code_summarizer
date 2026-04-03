# config.py
"""
Configuration settings for the Hybrid Code Summarizer
"""

# Model settings
DEFAULT_MODEL = "Salesforce/codet5-small"
TRAINED_MODEL_PATH = "./data/models/custom_summarizer"
MAX_CODE_LENGTH = 512
MAX_SUMMARY_LENGTH = 128

# AST Analysis settings
COMPLEXITY_THRESHOLDS = {
    'low': 5,
    'medium': 10,
    'high': 20
}

# Security patterns to detect
SECURITY_PATTERNS = {
    'dangerous_functions': ['eval', 'exec', '__import__', 'open', 'os.system', 'subprocess'],
    'network_indicators': ['requests', 'urllib', 'socket', 'http'],
    'crypto_indicators': ['hashlib', 'cryptography', 'secrets'],
    'file_operations': ['open', 'read', 'write', 'delete', 'remove']
}

# Training settings
TRAINING_CONFIG = {
    'batch_size': 4,
    'epochs': 3,
    'learning_rate': 3e-5,
    'validation_split': 0.2
}

# Output settings
REPORT_FORMAT = 'detailed'  # 'simple', 'detailed', 'security_focused'