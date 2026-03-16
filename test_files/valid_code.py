"""Sample valid Python code for testing"""
import math
import os

class Calculator:
    """A simple calculator class"""
    
    def add(self, a, b):
        """Add two numbers"""
        return a + b
    
    def multiply(self, a, b):
        """Multiply two numbers"""
        return a * b

def calculate_area(radius):
    """Calculate circle area"""
    return math.pi * radius ** 2

def read_file(filename):
    """Read a file and return contents"""
    with open(filename, 'r') as f:
        return f.read()