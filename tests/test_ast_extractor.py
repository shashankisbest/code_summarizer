"""Unit tests for AST Extractor module"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from ast_extractor import ASTExtractor

class TestASTExtractor:
    """Test suite for ASTExtractor class"""
    
    def test_extract_single_function(self):
        """Test extracting a single function"""
        code = """
def hello():
    print("Hello World")
"""
        extractor = ASTExtractor(code)
        functions = extractor.extract_functions()
        
        assert len(functions) == 1
        assert functions[0]['name'] == 'hello'
        assert functions[0]['args'] == []
        assert functions[0]['line_number'] == 2
    
    def test_extract_function_with_parameters(self):
        """Test extracting function with parameters"""
        code = """
def add(a, b, c):
    return a + b + c
"""
        extractor = ASTExtractor(code)
        functions = extractor.extract_functions()
        
        assert len(functions) == 1
        assert functions[0]['name'] == 'add'
        assert functions[0]['args'] == ['a', 'b', 'c']
    
    def test_extract_function_with_docstring(self):
        """Test extracting function with docstring"""
        code = '''
def greet(name):
    """Greet a person by name"""
    return f"Hello {name}"
'''
        extractor = ASTExtractor(code)
        functions = extractor.extract_functions()
        
        assert len(functions) == 1
        assert functions[0]['docstring'] == "Greet a person by name"
    
    def test_extract_multiple_functions(self):
        """Test extracting multiple functions"""
        code = """
def func1():
    pass

def func2(x):
    pass

def func3(x, y, z):
    pass
"""
        extractor = ASTExtractor(code)
        functions = extractor.extract_functions()
        
        assert len(functions) == 3
        assert functions[0]['name'] == 'func1'
        assert functions[1]['name'] == 'func2'
        assert functions[2]['name'] == 'func3'
    
    def test_extract_class(self):
        """Test extracting a class"""
        code = """
class MyClass:
    def method1(self):
        pass
    
    def method2(self, x):
        pass
"""
        extractor = ASTExtractor(code)
        classes = extractor.extract_classes()
        
        assert len(classes) == 1
        assert classes[0]['name'] == 'MyClass'
        assert 'method1' in classes[0]['methods']
        assert 'method2' in classes[0]['methods']
    
    def test_extract_imports(self):
        """Test extracting imports"""
        code = """
import os
import sys
from pathlib import Path
from collections import defaultdict, Counter
"""
        extractor = ASTExtractor(code)
        imports = extractor.extract_imports()
        
        assert 'os' in imports
        assert 'sys' in imports
        assert 'pathlib.Path' in imports
        assert 'collections.defaultdict' in imports
        assert 'collections.Counter' in imports
    
    def test_empty_code(self):
        """Test with empty code"""
        code = ""
        extractor = ASTExtractor(code)
        functions = extractor.extract_functions()
        classes = extractor.extract_classes()
        imports = extractor.extract_imports()
        
        assert len(functions) == 0
        assert len(classes) == 0
        assert len(imports) == 0
    
    def test_syntax_error(self):
        """Test that syntax errors are raised"""
        code = """
def broken(
    print("missing closing paren")
"""
        with pytest.raises(SyntaxError):
            extractor = ASTExtractor(code)


if __name__ == "__main__":
    pytest.main([__file__, '-v'])