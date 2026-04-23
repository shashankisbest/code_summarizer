import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.ast_analyzer import ASTAnalyzer

class TestASTAnalyzer:
    
    def test_extract_functions_simple(self):
        """Test extracting functions from simple code"""
        code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)
"""
        analyzer = ASTAnalyzer()
        result = analyzer.analyze(code)
        
        assert 'functions' in result
        assert len(result['functions']) == 1
        assert result['functions'][0]['name'] == 'factorial'
    
    def test_extract_classes(self):
        """Test extracting classes"""
        code = """
class Calculator:
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b
"""
        analyzer = ASTAnalyzer()
        result = analyzer.analyze(code)
        
        assert 'classes' in result
        assert len(result['classes']) == 1
        assert result['classes'][0]['name'] == 'Calculator'
        assert len(result['classes'][0]['methods']) == 2
    
    def test_extract_imports(self):
        """Test extracting imports"""
        code = """
import math
import os
from flask import Flask
import json
"""
        analyzer = ASTAnalyzer()
        result = analyzer.analyze(code)
        
        assert 'imports' in result
        assert len(result['imports'].get('direct', [])) >= 2
        assert len(result['imports'].get('from', [])) >= 1
    
    def test_complexity_calculation(self):
        """Test complexity metrics"""
        code = """
def complex_function(x):
    if x > 0:
        for i in range(10):
            if i % 2 == 0:
                print(i)
    return x
"""
        analyzer = ASTAnalyzer()
        result = analyzer.analyze(code)
        
        assert 'complexity' in result
        assert result['complexity']['cyclomatic'] >= 3
        assert result['complexity']['level'] in ['low', 'medium', 'high']
    
    def test_empty_code(self):
        """Test empty code handling"""
        code = ""
        analyzer = ASTAnalyzer()
        result = analyzer.analyze(code)
        
        assert 'error' not in result
        assert len(result.get('functions', [])) == 0
    
    def test_syntax_error(self):
        """Test invalid syntax handling"""
        code = "def broken function("
        analyzer = ASTAnalyzer()
        result = analyzer.analyze(code)
        
        assert 'error' in result