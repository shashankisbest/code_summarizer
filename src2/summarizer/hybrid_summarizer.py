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
        
        # For debugging - print what we're sending
        print(f"   🤖 Sending to ML: {enriched_input[:200]}...")
        
        try:
            summary = self.ml_model.generate(enriched_input, max_length=150)
            
            # Clean up the summary
            summary = summary.strip()
            
            # Remove any "summarize:" prefix
            if summary.lower().startswith("summarize:"):
                summary = summary[9:].strip()
            
            # If summary is still just repeating the input, use template
            if len(summary) < 20 or summary.startswith("This Python code has"):
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
        
        # Check for specific patterns from imports and calls
        imports_str = str(ast_data.get('imports', {}))
        calls_str = str(ast_data.get('calls', []))
        func_names = [f['name'] for f in ast_data.get('functions', [])]
        
        if 'factorial' in func_names or 'math' in imports_str:
            parts.append("mathematical calculations")
        elif 'threading' in imports_str or 'queue' in imports_str:
            parts.append("multi-threaded processing")
        elif 'json' in imports_str:
            parts.append("JSON data handling")
        elif 'hashlib' in imports_str:
            parts.append("cryptographic operations")
        elif 'sqlite3' in imports_str:
            parts.append("database operations")
        elif 'flask' in imports_str:
            parts.append("web application")
        
        if parts:
            return "A Python module that " + " and ".join(parts) + "."
        else:
            return "Python module with various functions and classes."
    
    def _create_enriched_input(self, code: str, ast_data: Dict, security_data: Dict) -> str:
        """
        Create detailed prompt for T5 to generate meaningful summary
        """
        # Extract basic info
        func_names = [f['name'] for f in ast_data.get('functions', [])[:5]]
        class_names = [c['name'] for c in ast_data.get('classes', [])[:3]]
        
        # Analyze imports to detect purpose
        imports_str = str(ast_data.get('imports', {}))
        calls_str = str(ast_data.get('calls', []))
        
        # Detect what the code does
        purpose_keywords = []
        
        if 'flask' in imports_str or 'app.route' in code:
            purpose_keywords.append("web application with API endpoints")
        elif 'django' in imports_str:
            purpose_keywords.append("Django web framework")
        
        if 'sqlite3' in imports_str or 'mysql' in imports_str or 'postgres' in imports_str:
            purpose_keywords.append("database operations")
        
        if 'threading' in imports_str or 'queue' in imports_str:
            purpose_keywords.append("multi-threaded processing")
        
        if 'hashlib' in imports_str or 'cryptography' in imports_str:
            purpose_keywords.append("cryptographic hashing and security")
        
        if 'json' in imports_str:
            purpose_keywords.append("JSON data handling")
        
        if 'math' in imports_str or 'factorial' in func_names:
            purpose_keywords.append("mathematical calculations")
        
        if 'requests' in imports_str or 'urllib' in imports_str:
            purpose_keywords.append("HTTP requests and API calls")
        
        if 'pandas' in imports_str or 'numpy' in imports_str:
            purpose_keywords.append("data analysis and manipulation")
        
        if 'exec' in calls_str or 'eval' in calls_str:
            purpose_keywords.append("⚠️ WARNING: dynamic code execution")
        
        # Check for SQL injection patterns
        if 'f"SELECT' in code or '.format(' in code and 'SELECT' in code:
            purpose_keywords.append("⚠️ POTENTIAL SQL INJECTION VULNERABILITY")
        
        # Build the prompt
        if purpose_keywords:
            purpose_text = ", ".join(purpose_keywords)
            prompt = f"""This Python code performs {purpose_text}. It contains functions: {', '.join(func_names)} and classes: {', '.join(class_names)}.
            
Describe what this code does in 2-3 sentences:"""
        else:
            # Fallback - analyze function names
            if func_names:
                prompt = f"""This Python code has functions named {', '.join(func_names)}.
Based on these function names, describe what this code likely does:"""
            else:
                prompt = f"""This Python code has {len(ast_data.get('functions', []))} functions and {len(ast_data.get('classes', []))} classes.
Describe what this code does:"""
        
        return prompt