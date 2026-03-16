from summarizer import CodeSummarizer
from ml_summarizer import MLCodeSummarizer
import ast

class HybridSummarizer:
    """
    Combines template-based and ML-based summarization.
    Provides comparison between both approaches.
    """
    
    def __init__(self, source_code, use_ml=True):
        self.source_code = source_code
        self.use_ml = use_ml
        
        # Initialize template-based summarizer
        self.template_summarizer = CodeSummarizer(source_code)
        
        # Initialize ML summarizer if requested
        self.ml_summarizer = None
        if use_ml:
            try:
                self.ml_summarizer = MLCodeSummarizer()
            except Exception as e:
                print(f"⚠️  Warning: Could not load ML model: {e}")
                print("   Falling back to template-based only.")
                self.use_ml = False
    
    def generate_comparison_report(self):
        """Generate a report comparing both summarization methods"""
        
        lines = []
        lines.append("=" * 70)
        lines.append("HYBRID CODE SUMMARY REPORT")
        lines.append("Template-Based + ML-Based Comparison")
        lines.append("=" * 70)
        lines.append("")
        
        # Get template-based summary
        template_summary = self.template_summarizer.generate_full_summary()
        
        # File-level ML summary
        if self.use_ml and self.ml_summarizer:
            lines.append("🤖 ML-GENERATED FILE SUMMARY:")
            ml_file_summary = self.ml_summarizer.summarize_entire_file(self.source_code)
            lines.append(f"   {ml_file_summary}")
            lines.append("")
        
        lines.append("-" * 70)
        lines.append("TEMPLATE-BASED ANALYSIS:")
        lines.append("-" * 70)
        lines.append(template_summary)
        
        # If ML is enabled, add ML summaries for functions
        if self.use_ml and self.ml_summarizer:
            lines.append("\n" + "=" * 70)
            lines.append("🤖 ML-ENHANCED FUNCTION SUMMARIES:")
            lines.append("=" * 70)
            lines.append("")
            
            # Extract functions from source code
            tree = ast.parse(self.source_code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Get the function's source code
                    func_lines = self.source_code.split('\n')[node.lineno-1:node.end_lineno]
                    func_code = '\n'.join(func_lines)
                    
                    # Generate ML summary
                    ml_summary = self.ml_summarizer.summarize_function(func_code, node.name)
                    lines.append(f"   • {ml_summary}")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def generate_ml_only_summary(self):
        """Generate summary using only ML model"""
        if not self.use_ml or not self.ml_summarizer:
            return "ML summarization not available."
        
        lines = []
        lines.append("=" * 70)
        lines.append("🤖 ML-BASED CODE SUMMARY")
        lines.append("=" * 70)
        lines.append("")
        
        # File-level summary
        lines.append("📋 FILE PURPOSE:")
        ml_summary = self.ml_summarizer.summarize_entire_file(self.source_code)
        lines.append(f"   {ml_summary}")
        lines.append("")
        
        # Function summaries
        tree = ast.parse(self.source_code)
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        
        if functions:
            lines.append("⚙️  FUNCTIONS:")
            for node in functions:
                func_lines = self.source_code.split('\n')[node.lineno-1:node.end_lineno]
                func_code = '\n'.join(func_lines)
                ml_summary = self.ml_summarizer.summarize_function(func_code, node.name)
                lines.append(f"   • {ml_summary}")
            lines.append("")
        
        # Classes
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        if classes:
            lines.append("🏗️  CLASSES:")
            for node in classes:
                class_lines = self.source_code.split('\n')[node.lineno-1:node.end_lineno]
                class_code = '\n'.join(class_lines)
                ml_summary = self.ml_summarizer.summarize_class(class_code, node.name)
                lines.append(f"   • {ml_summary}")
            lines.append("")
        
        lines.append("=" * 70)
        return "\n".join(lines)


# Test
if __name__ == "__main__":
    test_code = """
import hashlib

class UserAuthenticator:
    def hash_password(self, password):
        '''Hash password using SHA256'''
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password, hash_value):
        '''Verify if password matches hash'''
        return self.hash_password(password) == hash_value

def create_user(username, password):
    '''Create a new user account'''
    auth = UserAuthenticator()
    hashed = auth.hash_password(password)
    return {'username': username, 'password_hash': hashed}
"""
    
    print("\n🔄 Testing Hybrid Summarizer...\n")
    
    hybrid = HybridSummarizer(test_code, use_ml=True)
    report = hybrid.generate_comparison_report()
    print(report)