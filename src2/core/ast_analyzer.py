# core/ast_analyzer.py
"""
Enhanced AST-based code analyzer
Extracts structural patterns, complexity metrics, and code relationships
"""

import ast
import inspect
from typing import List, Dict, Set, Any
import re

class ASTAnalyzer:
    """
    Advanced AST extractor that captures:
    - Functions, classes, imports
    - Complexity metrics
    - Code relationships
    - Data flow patterns
    """
    
    def __init__(self):
        self.ast_tree = None
        self.source_code = None
        
    def analyze(self, source_code: str) -> Dict[str, Any]:
        """
        Analyze source code and return comprehensive AST data
        """
        self.source_code = source_code
        
        try:
            self.ast_tree = ast.parse(source_code)
        except SyntaxError as e:
            return {'error': f"Syntax error: {e}"}
        
        analysis = {
            'functions': self._extract_functions(),
            'classes': self._extract_classes(),
            'imports': self._extract_imports(),
            'complexity': self._calculate_complexity(),
            'relationships': self._find_relationships(),
            'calls': self._extract_function_calls(),
            'variables': self._extract_variables(),
            'decorators': self._extract_decorators(),
            'line_count': len(self.source_code.split('\n')),
            'has_main': self._has_main_block()
        }
        
        return analysis
    
    def _extract_functions(self) -> List[Dict]:
        """Extract all functions with their details"""
        functions = []
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    'name': node.name,
                    'params': [arg.arg for arg in node.args.args],
                    'returns': self._get_return_type(node),
                    'line_start': node.lineno,
                    'line_end': node.end_lineno if hasattr(node, 'end_lineno') else node.lineno,
                    'decorators': [self._get_decorator_name(d) for d in node.decorator_list],
                    'docstring': ast.get_docstring(node),
                    'complexity': self._calculate_function_complexity(node),
                    'calls': self._get_function_calls(node),
                    'is_recursive': self._is_recursive(node)
                }
                functions.append(func_info)
        
        return functions
    
    def _extract_classes(self) -> List[Dict]:
        """Extract all classes with their methods and attributes"""
        classes = []
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.ClassDef):
                class_info = {
                    'name': node.name,
                    'methods': [],
                    'attributes': [],
                    'bases': [self._get_base_name(base) for base in node.bases],
                    'line_start': node.lineno,
                    'line_end': node.end_lineno if hasattr(node, 'end_lineno') else node.lineno,
                    'docstring': ast.get_docstring(node)
                }
                
                # Extract methods
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_info = {
                            'name': item.name,
                            'params': [arg.arg for arg in item.args.args],
                            'is_static': '@staticmethod' in [self._get_decorator_name(d) for d in item.decorator_list],
                            'is_classmethod': '@classmethod' in [self._get_decorator_name(d) for d in item.decorator_list]
                        }
                        class_info['methods'].append(method_info)
                    
                    elif isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Name):
                                class_info['attributes'].append(target.id)
                
                classes.append(class_info)
        
        return classes
    
    def _extract_imports(self) -> Dict[str, List[str]]:
        """Extract all imports"""
        imports = {
            'direct': [],
            'from': []
        }
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports['direct'].append(alias.name)
            
            elif isinstance(node, ast.ImportFrom):
                module = node.module
                for alias in node.names:
                    imports['from'].append(f"{module}.{alias.name}")
        
        return imports
    
    def _calculate_complexity(self) -> Dict[str, Any]:
        """Calculate complexity metrics with proper maintainability index"""
        
        cyclomatic = self._calculate_cyclomatic_complexity()
        cognitive = self._calculate_cognitive_complexity()
        loc = len(self.source_code.split('\n'))
        
        # Maintainability Index formula (standard)
        # MI = 171 - 5.2 * ln(V) - 0.23 * V(g) - 16.2 * ln(LOC)
        import math
        
        if cyclomatic > 0 and loc > 0:
            try:
                maintainability = 171 - (5.2 * math.log(cyclomatic)) - (0.23 * cyclomatic) - (16.2 * math.log(loc))
                maintainability = max(0, min(100, maintainability))
            except:
                maintainability = 50.0  # Default fallback
        else:
            maintainability = 50.0
        
        # Determine level
        if cyclomatic <= 5:
            level = 'low'
        elif cyclomatic <= 10:
            level = 'medium'
        else:
            level = 'high'
        
        return {
            'cyclomatic': cyclomatic,
            'cognitive': cognitive,
            'maintainability': round(maintainability, 1),
            'level': level
        }
    
    def _calculate_cyclomatic_complexity(self) -> int:
        """Calculate cyclomatic complexity (McCabe's metric)"""
        complexity = 1  # Base complexity
        
        for node in ast.walk(self.ast_tree):
            # Decision points that increase complexity
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                # Each boolean operator increases complexity
                complexity += len(node.values) - 1
            elif isinstance(node, ast.And) or isinstance(node, ast.Or):
                complexity += 1
        
        return complexity
    
    def _calculate_cognitive_complexity(self) -> int:
        """Calculate cognitive complexity (how hard to understand)"""
        complexity = 0
        nesting_depth = 0
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, (ast.If, ast.While, ast.For)):
                complexity += 1 + nesting_depth
                nesting_depth += 1
            elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                nesting_depth = 0
        
        return complexity
    
    def _find_relationships(self) -> Dict[str, List[str]]:
        """Find relationships between components"""
        relationships = {
            'calls': [],      # function calls
            'inherits': [],   # class inheritance
            'uses': []        # variable usage
        }
        
        functions = [f['name'] for f in self._extract_functions()]
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in functions:
                        relationships['calls'].append(node.func.id)
        
        return relationships
    
    def _extract_function_calls(self) -> List[str]:
        """Extract all function calls in the code"""
        calls = []
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    calls.append(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    calls.append(node.func.attr)
        
        return list(set(calls))
    
    def _extract_variables(self) -> List[str]:
        """Extract variable names"""
        variables = set()
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.Name):
                if isinstance(node.ctx, (ast.Store, ast.Load)):
                    variables.add(node.id)
        
        return list(variables)
    
    def _extract_decorators(self) -> List[str]:
        """Extract decorators used"""
        decorators = []
        
        for node in ast.walk(self.ast_tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                for decorator in node.decorator_list:
                    decorators.append(self._get_decorator_name(decorator))
        
        return list(set(decorators))
    
    def _has_main_block(self) -> bool:
        """Check if code has if __name__ == '__main__' block"""
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.If):
                if isinstance(node.test, ast.Compare):
                    if (isinstance(node.test.left, ast.Name) and 
                        node.test.left.id == '__name__'):
                        return True
        return False
    
    def _calculate_function_complexity(self, func_node) -> int:
        """Calculate complexity for a single function"""
        complexity = 1
        
        for node in ast.walk(func_node):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
        
        return complexity
    
    def _get_return_type(self, func_node) -> str:
        """Try to infer return type"""
        returns = []
        
        for node in ast.walk(func_node):
            if isinstance(node, ast.Return):
                if node.value:
                    if isinstance(node.value, ast.Constant):
                        returns.append(type(node.value.value).__name__)
        
        return list(set(returns)) if returns else ['unknown']
    
    def _get_function_calls(self, func_node) -> List[str]:
        """Get function calls within a function"""
        calls = []
        
        for node in ast.walk(func_node):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    calls.append(node.func.id)
        
        return list(set(calls))
    
    def _is_recursive(self, func_node) -> bool:
        """Check if function is recursive"""
        func_name = func_node.name
        calls = self._get_function_calls(func_node)
        return func_name in calls
    
    def _get_decorator_name(self, decorator) -> str:
        """Extract decorator name"""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return decorator.attr
        return 'unknown'
    
    def _get_base_name(self, base) -> str:
        """Extract base class name"""
        if isinstance(base, ast.Name):
            return base.id
        elif isinstance(base, ast.Attribute):
            return base.attr
        return 'unknown'