import os

def read_file(filepath):
    try:
        with open(filepath, 'r') as file:
            return file.readlines()
    except IOError:
        print("Error reading file")
        return []

def count_words(lines):
    word_count = 0
    for line in lines:
        words = line.split()
        word_count += len(words)
    return word_count

class FileAnalyzer:
    
    def __init__(self, filepath):
        self.filepath = filepath
    
    def analyze(self):
        lines = read_file(self.filepath)
        return count_words(lines)