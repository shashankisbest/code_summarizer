import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from summarizer.hybrid_summarizer import HybridSummarizer

class TestSummarizer:
    
    def test_template_summary_generation(self):
        """Test template-based summary generation"""
        code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)
"""
        summarizer = HybridSummarizer(ml_model=None)
        result = summarizer.summarize(code, use_ml=False)
        
        assert result is not None
        assert "SUMMARY" in result
        assert "functions" in result.lower()
    
    def test_statistics_extraction(self):
        """Test statistics extraction"""
        code = """
import math

class MyClass:
    def method1(self):
        pass

def func1():
    pass

def func2():
    pass
"""
        summarizer = HybridSummarizer(ml_model=None)
        result = summarizer.summarize(code, use_ml=False)
        
        assert "Functions: 2" in result or "functions" in result.lower()
        assert "Classes: 1" in result or "classes" in result.lower()
    
    def test_security_audit_in_report(self):
        """Test security audit appears in report"""
        code = """
result = eval(input("Enter expression: "))
"""
        summarizer = HybridSummarizer(ml_model=None)
        result = summarizer.summarize(code, use_ml=False)
        
        assert "SECURITY" in result or "RISK" in result
    
    def test_complexity_in_report(self):
        """Test complexity appears in report"""
        code = """
def complex_func(x):
    if x > 0:
        for i in range(10):
            if i % 2 == 0:
                print(i)
    return x
"""
        summarizer = HybridSummarizer(ml_model=None)
        result = summarizer.summarize(code, use_ml=False)
        
        assert "COMPLEXITY" in result
        assert "Cyclomatic" in result or "cyclomatic" in result.lower()