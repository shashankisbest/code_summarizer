# summarizer/hybrid_summarizer.py
"""
Main hybrid summarizer combining AST analysis with ML generation
"""
from typing import Dict, Any, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.ast_analyzer import ASTAnalyzer
from core.security_scanner import SecurityScanner
from summarizer.report_generator import ReportGenerator

class HybridSummarizer:
    """
    Combines AST analysis with ML-generated summaries
    for comprehensive code understanding
    """
    
    def __init__(self, ml_model=None):
        """
        Initialize with optional ML model
        """
        self.ast_analyzer = ASTAnalyzer()
        self.security_scanner = SecurityScanner()
        self.report_generator = ReportGenerator()
        self.ml_model = ml_model
        
    def summarize(self, source_code: str, use_ml: bool = True):
        """
        Generate comprehensive summary of code
        
        Args:
            source_code: Python source code as string
            use_ml: Whether to use ML model for summary generation
            
        Returns:
            Dictionary with complete analysis and summary
        """
        print("🔍 Analyzing code with AST...")
        
        # Step 1: AST Analysis
        ast_analysis = self.ast_analyzer.analyze(source_code)
        
        if 'error' in ast_analysis:
            return {'error': ast_analysis['error']}
        
        # Step 2: Security Scan
        print("🔒 Scanning for security issues...")
        security_findings = self.security_scanner.scan(source_code, ast_analysis)
        
        # Step 3: Generate Summary
        print("📝 Generating summary...")
        
        if use_ml and self.ml_model and self.ml_model.is_available():
            ml_summary = self._generate_ml_summary(source_code, ast_analysis, security_findings)
        else:
            ml_summary = self._generate_template_summary(ast_analysis)
        
        # Step 4: Create comprehensive report
        print("📊 Creating final report...")
        report = self.report_generator.generate_report(
            ast_analysis=ast_analysis,
            security_findings=security_findings,
            ml_summary=ml_summary,
            source_code=source_code
        )
        
        return report
    
    def _generate_ml_summary(self, code: str, ast_data: Dict, security_data: Dict) -> str:
        """
        Generate summary using ML model with AST context
        """
        if not self.ml_model or not self.ml_model.is_available():
            return "ML model not available - using template mode"
        
        # Create enriched input with AST data
        enriched_input = self._create_enriched_input(code, ast_data, security_data)
        
        try:
            summary = self.ml_model.generate(enriched_input, max_length=80)
            
            # If summary is the fallback message, return template instead
            if summary == "Code analysis complete." or len(summary) < 15:
                return self._generate_template_summary(ast_data)
            
            return summary
            
        except Exception as e:
            return f"[ML Error: {e}]"
    
    def _generate_template_summary(self, ast_data: Dict) -> str:
        """
        Generate summary using template-based approach
        """
        parts = []
        
        # Describe components
        if ast_data.get('functions'):
            func_count = len(ast_data['functions'])
            parts.append(f"contains {func_count} function{'s' if func_count > 1 else ''}")
        
        if ast_data.get('classes'):
            class_count = len(ast_data['classes'])
            parts.append(f"{class_count} class{'es' if class_count > 1 else ''}")
        
        # Describe complexity
        complexity = ast_data.get('complexity', {}).get('level', 'unknown')
        parts.append(f"{complexity} complexity")
        
        # Describe purpose based on patterns
        if ast_data.get('has_main'):
            parts.append("executable script")
        
        # Check for specific patterns
        all_calls = str(ast_data.get('calls', []))
        if 'factorial' in all_calls or 'math' in all_calls:
            parts.append("mathematical computations")
        elif 'threading' in all_calls or 'queue' in all_calls:
            parts.append("multi-threaded processing")
        elif 'json' in all_calls:
            parts.append("JSON data handling")
        elif 'hashlib' in all_calls:
            parts.append("cryptographic operations")
        
        if parts:
            return "A Python module that " + " and ".join(parts) + "."
        else:
            return "Python module with various functions and classes."
    
# Inside hybrid_summarizer.py - replace _create_enriched_input method

    def _create_enriched_input(self, code: str, ast_data: Dict, security_data: Dict) -> str:
        """
        Create prompt optimized for CodeParrot
        """
        # Extract key information
        func_names = [f['name'] for f in ast_data.get('functions', [])[:10]]
        class_names = [c['name'] for c in ast_data.get('classes', [])[:5]]
        
        # Detect main purpose
        imports_str = str(ast_data.get('imports', {}))
        
        purpose = []
        if 'threading' in imports_str or 'queue' in imports_str:
            purpose.append("multi-threaded data processing")
        if 'json' in imports_str:
            purpose.append("JSON handling")
        if 'math' in imports_str:
            purpose.append("mathematical calculations")
        if 'functools' in imports_str:
            purpose.append("function memoization and caching")
        if 'random' in imports_str:
            purpose.append("random data generation")
        if 'time' in imports_str:
            purpose.append("timing and delays")
        
        purpose_text = ", ".join(purpose) if purpose else "various operations"
        
        # Build compact prompt for CodeParrot
        prompt = f"""a Python module with these components:
    - Functions: {', '.join(func_names[:8])}
    - Classes: {', '.join(class_names)}
    - Imports: threading, queue, math, json, random, time, functools
    - Complexity: {ast_data.get('complexity', {}).get('level', 'medium')}

    This code implements {purpose_text}. It"""
        
        return prompt