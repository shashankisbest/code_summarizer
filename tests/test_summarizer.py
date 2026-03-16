"""Unit tests for Code Summarizer module"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from summarizer import CodeSummarizer

class TestCodeSummarizer:
    """Test suite for CodeSummarizer class"""
    
    def test_summarize_simple_function(self):
        """Test summarizing a simple function"""
        code = """
def hello():
    '''Say hello'''
    print("Hello")
"""
        summarizer = CodeSummarizer(code)
        func_info = {'name': 'hello', 'args': [], 'docstring': 'Say hello'}
        summary = summarizer.summarize_function(func_info)
        
        assert 'hello' in summary
        assert 'Say hello' in summary
    
    def test_summarize_class(self):
        """Test summarizing a class"""
        code = """
class Calculator:
    def add(self, a, b):
        return a + b
    def subtract(self, a, b):
        return a - b
"""
        summarizer = CodeSummarizer(code)
        class_info = {'name': 'Calculator', 'methods': ['add', 'subtract'], 'line_number': 2}
        summary = summarizer.summarize_class(class_info)
        
        assert 'Calculator' in summary
        assert '2 methods' in summary
    
    def test_analyze_complexity_no_control_flow(self):
        """Test complexity analysis with no control flow"""
        code = """
def simple():
    x = 1
    y = 2
    return x + y
"""
        summarizer = CodeSummarizer(code)
        complexity = summarizer.analyze_complexity()
        
        assert complexity['if_statements'] == 0
        assert complexity['loops'] == 0
        assert complexity['try_except'] == 0
    
    def test_analyze_complexity_with_control_flow(self):
        """Test complexity analysis with control flow"""
        code = """
def complex_function(x):
    if x > 0:
        for i in range(x):
            print(i)
    
    try:
        result = 10 / x
    except ZeroDivisionError:
        result = 0
    
    return result
"""
        summarizer = CodeSummarizer(code)
        complexity = summarizer.analyze_complexity()
        
        assert complexity['if_statements'] == 1
        assert complexity['loops'] == 1
        assert complexity['try_except'] == 1
    
    def test_determine_purpose_data_science(self):
        """Test purpose detection for data science code"""
        code = """
import pandas as pd
import numpy as np
import sklearn

def analyze():
    pass
"""
        summarizer = CodeSummarizer(code)
        purpose = summarizer.determine_purpose()
        
        assert 'data analysis' in purpose.lower() or 'machine learning' in purpose.lower()
    
    def test_determine_purpose_web(self):
        """Test purpose detection for web code"""
        code = """
from flask import Flask

app = Flask(__name__)
"""
        summarizer = CodeSummarizer(code)
        purpose = summarizer.determine_purpose()
        
        assert 'web' in purpose.lower()
    
    def test_audit_notes_security_warning(self):
        """Test security warnings in audit notes"""
        code = """
import subprocess

def run_command(cmd):
    subprocess.call(cmd, shell=True)
"""
        summarizer = CodeSummarizer(code)
        notes = summarizer.generate_audit_notes()
        
        # Should warn about subprocess
        assert any('subprocess' in note.lower() or 'system command' in note.lower() for note in notes)
    
    def test_audit_notes_eval_warning(self):
        """Test warning for eval usage"""
        code = """
def dangerous(user_input):
    return eval(user_input)
"""
        summarizer = CodeSummarizer(code)
        notes = summarizer.generate_audit_notes()
        
        # Should warn about eval
        assert any('eval' in note.lower() for note in notes)
    
    def test_full_summary_generation(self):
        """Test full summary report generation"""
        code = """
import math

class Circle:
    def area(self, radius):
        return math.pi * radius ** 2

def main():
    c = Circle()
    print(c.area(5))
"""
        summarizer = CodeSummarizer(code)
        summary = summarizer.generate_full_summary()
        
        # Check that all sections are present
        assert 'PURPOSE' in summary
        assert 'STATISTICS' in summary
        assert 'COMPLEXITY' in summary
        assert 'CLASSES' in summary
        assert 'FUNCTIONS' in summary
        assert 'AUDIT NOTES' in summary


if __name__ == "__main__":
    pytest.main([__file__, '-v'])