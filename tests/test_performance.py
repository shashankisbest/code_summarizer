"""Performance benchmarks for code summarization"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import time
from summarizer import CodeSummarizer

class TestPerformance:
    """Performance and speed benchmarks"""
    
    def test_single_file_speed(self):
        """Benchmark: How fast is single file analysis?"""
        code = """
import math

def calculate_area(radius):
    return math.pi * radius ** 2

class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return calculate_area(self.radius)
"""
        
        start = time.time()
        summarizer = CodeSummarizer(code)
        summary = summarizer.generate_full_summary()
        elapsed = time.time() - start
        
        print(f"\n⏱️  Single file analysis: {elapsed:.4f} seconds")
        assert elapsed < 1.0, "Should complete in under 1 second"
    
    def test_batch_processing_speed(self):
        """Benchmark: How fast is batch processing?"""
        code = """
def test_function(x, y):
    return x + y
"""
        
        num_files = 100
        start = time.time()
        
        for i in range(num_files):
            summarizer = CodeSummarizer(code)
            summary = summarizer.generate_full_summary()
        
        elapsed = time.time() - start
        per_file = elapsed / num_files
        
        print(f"\n⏱️  Batch processing ({num_files} files):")
        print(f"   Total time: {elapsed:.2f} seconds")
        print(f"   Per file: {per_file:.4f} seconds")
        print(f"   Throughput: {num_files/elapsed:.1f} files/second")
        
        assert elapsed < 10.0, "Should process 100 files in under 10 seconds"
    
    def test_large_file_handling(self):
        """Benchmark: How does it handle large files?"""
        # Generate a large file with many functions
        code_lines = ["import os", "import sys", ""]
        
        for i in range(50):  # 50 functions
            code_lines.append(f"def function_{i}(x, y):")
            code_lines.append(f"    '''Function number {i}'''")
            code_lines.append(f"    return x + y + {i}")
            code_lines.append("")
        
        code = "\n".join(code_lines)
        
        start = time.time()
        summarizer = CodeSummarizer(code)
        summary = summarizer.generate_full_summary()
        elapsed = time.time() - start
        
        print(f"\n⏱️  Large file (50 functions): {elapsed:.4f} seconds")
        assert elapsed < 2.0, "Should handle large files in under 2 seconds"
    
    def test_complexity_analysis_overhead(self):
        """Benchmark: Complexity analysis impact on speed"""
        code_simple = "x = 1"
        
        code_complex = """
for i in range(100):
    if i % 2 == 0:
        for j in range(100):
            try:
                result = i / j
            except:
                pass
"""
        
        # Simple code
        start = time.time()
        s1 = CodeSummarizer(code_simple)
        c1 = s1.analyze_complexity()
        time_simple = time.time() - start
        
        # Complex code
        start = time.time()
        s2 = CodeSummarizer(code_complex)
        c2 = s2.analyze_complexity()
        time_complex = time.time() - start
        
        print(f"\n⏱️  Complexity Analysis:")
        print(f"   Simple code: {time_simple:.4f} seconds")
        print(f"   Complex code: {time_complex:.4f} seconds")
        print(f"   Overhead: {(time_complex - time_simple):.4f} seconds")


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, '-v', '-s'])  # -s shows print output