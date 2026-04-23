"""Integration tests for the entire pipeline"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from summarizer import CodeSummarizer

class TestIntegration:
    """End-to-end integration tests"""
    
    def test_valid_file_analysis(self):
        """Test analyzing a valid Python file"""
        test_file = os.path.join(os.path.dirname(__file__), '..', 'test_files', 'valid_code.py')
        
        with open(test_file, 'r') as f:
            code = f.read()
        
        summarizer = CodeSummarizer(code)
        summary = summarizer.generate_full_summary()
        
        # Should find the Calculator class
        assert 'Calculator' in summary
        # Should find functions
        assert 'calculate_area' in summary or 'read_file' in summary
        # Should detect math import
        assert 'math' in summary
    
    def test_security_file_detection(self):
        """Test security issue detection"""
        test_file = os.path.join(os.path.dirname(__file__), '..', 'test_files', 'security_issue.py')
        
        with open(test_file, 'r') as f:
            code = f.read()
        
        summarizer = CodeSummarizer(code)
        summary = summarizer.generate_full_summary()
        
        # Should detect security issues
        assert 'WARNING' in summary or 'CRITICAL' in summary
        # Should mention subprocess
        assert 'subprocess' in summary.lower() or 'system command' in summary.lower()
        # Should mention pickle
        assert 'pickle' in summary.lower()
        # Should mention eval
        assert 'eval' in summary.lower()
    
    def test_empty_file_handling(self):
        """Test handling of empty files"""
        code = "# Just a comment\n"
        
        summarizer = CodeSummarizer(code)
        summary = summarizer.generate_full_summary()
        
        # Should still generate a summary
        assert 'STATISTICS' in summary
        # Should show 0 functions
        assert 'Functions: 0' in summary
    
    def test_no_functions_file(self):
        """Test file with no functions"""
        test_file = os.path.join(os.path.dirname(__file__), '..', 'test_files', 'no_functions.py')
        
        with open(test_file, 'r') as f:
            code = f.read()
        
        summarizer = CodeSummarizer(code)
        summary = summarizer.generate_full_summary()
        
        # Should show 0 functions but still have imports
        assert 'Functions: 0' in summary
        assert 'sys' in summary or 'os' in summary


if __name__ == "__main__":
    pytest.main([__file__, '-v'])