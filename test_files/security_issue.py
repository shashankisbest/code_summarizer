"""File with security vulnerabilities"""
import subprocess
import pickle

def execute_command(cmd):
    """Dangerous function that executes shell commands"""
    return subprocess.call(cmd, shell=True)

def load_data(filename):
    """Dangerous function using pickle"""
    with open(filename, 'rb') as f:
        return pickle.load(f)

# Using eval - major security risk
user_input = "2 + 2"
result = eval(user_input)