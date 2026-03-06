import ast
import json

class ASTExtractor:

    def __init__(self,sourcecode):

        self.sourcecode = sourcecode
        self.tree = ast.parse(sourcecode)

    def extract_functions(self):
        functions = list()

        for node in ast.walk(self.tree): #traversing like a normal tree

            if isinstance(node,ast.FunctionDef):  #checking if node is a function or not


                '''it is checking if the node is of the datatype "FunctionDef"
                    other example:
                    x = 2
                    isinstance(x,int)
                '''


                information = {
                    'name' : node.name,
                    'args' : [argument.arg for argument in node.args.args ],
                    'line_number' : node.lineno,
                    'docstring' : ast.get_docstring(node)

                    
                }
                functions.append(information)

        return functions
    
    def extract_classes(self):

        classes = list()

        for node in ast.walk(self.tree):
            if isinstance(node,ast.ClassDef):
                
                information = {
                    'name' : node.name,
                    'methods' : [],
                    'line_number' : node.lineno
                }

                for item in node.body:
                    if isinstance(item,ast.FunctionDef):
                        information['methods'].append(item.name)

                classes.append(information)

        return classes


    def extract_imports(self):

        imports = list()

        for node in ast.walk(self.tree):
            if isinstance(node,ast.Import):

                for alias in node.names:
                    imports.append(alias.name)
            
            elif isinstance(node,ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}")

                    """module - string
                       alias.name - string
                    """

        return imports
    

    def get_summary_data(self):
        return {
            'functions' : self.extract_functions(),
            'classes' : self.extract_classes(),
            'imports' : self.extract_imports()
        }


if __name__ == "__main":
    # & sample code
    sourcecode = """
    import math
    import os

    class Calculator:
        def add(self, a, b):
            '''Add two numbers'''
            return a + b
        
        def multiply(self, a, b):
            '''Multiply two numbers'''
            return a * b

    def calculate_area(radius):
        '''Calculate circle area'''
        return math.pi * radius ** 2

    def main():
        calc = Calculator()
        result = calc.add(5, 3)
        print(result)

    """

    extractor = ASTExtractor(sourcecode)
    summary = extractor.get_summary_data()

    print("="*50)
    print("imports")
    print("="*50)

    for imp in summary['imports']:
        print(f" - {imp}")




    print("="*50)
    print("classes")
    print("="*50)
    for cls in summary['classes']:
        print(f" - {cls['name']} at line {cls['line_number']}")
        print(f" - methods: {cls['methods']}")


    print("="*50)
    print("functions")
    print("="*50)
    for fun in summary['functions']:
        print(f" - {fun['name']} at line {fun['line_number']} with args {fun['args']}")
        
        if fun['docstring']:print(f"Doc: {fun['docstring']}")


    print("&^&&^&^&^&^&^&&^&^&^&&^&^&&^&^")