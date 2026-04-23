import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from summarizer.hybrid_summarizer import HybridSummarizer
from core.ast_analyzer import ASTAnalyzer
from core.security_scanner import SecurityScanner

class TestIntegration:
    
    def test_full_pipeline_simple(self):
        """Test full pipeline with simple code"""
        code = """
def add(a, b):
    return a + b
"""
        # AST Analysis
        analyzer = ASTAnalyzer()
        ast_result = analyzer.analyze(code)
        
        # Security Scan
        scanner = SecurityScanner()
        security_result = scanner.scan(code, ast_result)
        
        # Summarizer
        summarizer = HybridSummarizer(ml_model=None)
        final_result = summarizer.summarize(code, use_ml=False)
        
        assert ast_result is not None
        assert security_result is not None
        assert final_result is not None
    
    def test_full_pipeline_with_imports(self):
        """Test full pipeline with imports"""
        code = """
import json
import requests

def fetch_data(url):
    response = requests.get(url)
    return json.loads(response.text)
"""
        summarizer = HybridSummarizer(ml_model=None)
        result = summarizer.summarize(code, use_ml=False)
        
        assert "imports" in result.lower() or "IMPORTS" in result
    
    def test_multiple_functions_detection(self):
        """Test detection of multiple functions"""
        code = """
def func1():
    pass

def func2():
    pass

def func3():
    pass
"""
        summarizer = HybridSummarizer(ml_model=None)
        result = summarizer.summarize(code, use_ml=False)
        
        # Should detect 3 functions
        assert "3" in result or "three" in result.lower()
    
    def test_end_to_end_with_security(self):
        """Test end-to-end with security vulnerability"""
        code = """
import os

def delete_files():
    os.system("rm -rf /tmp/*")
"""
        summarizer = HybridSummarizer(ml_model=None)
        result = summarizer.summarize(code, use_ml=False)
        
        assert "SECURITY" in result
        assert "os.system" in result or "RISK" in result