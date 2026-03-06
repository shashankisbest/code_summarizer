import ast
from ast_extractor import ASTExtractor

class CodeSummarizer:
    """Generates human-readable summaries from AST data"""
    
    def __init__(self, source_code):
        self.extractor = ASTExtractor(source_code)
        self.summary_data = self.extractor.get_summary_data()
        self.source_code = source_code
        self.tree = ast.parse(source_code)
    
    def analyze_complexity(self):
        """Analyze code complexity by counting control flow statements"""
        complexity_info = {
            'if_statements': 0,
            'loops': 0,
            'try_except': 0
        }
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.If):
                complexity_info['if_statements'] += 1
            elif isinstance(node, (ast.For, ast.While)):
                complexity_info['loops'] += 1
            elif isinstance(node, ast.Try):
                complexity_info['try_except'] += 1
        
        return complexity_info
    
    def summarize_function(self, func_info):
        """Generate a summary for a single function"""
        name = func_info['name']
        args = func_info['args']
        docstring = func_info['docstring']
        
        # Build summary
        if docstring:
            summary = f"Function '{name}': {docstring}"
        else:
            # Generate summary based on name and parameters
            param_count = len(args)
            
            if param_count == 0:
                summary = f"Function '{name}' takes no parameters"
            elif param_count == 1:
                summary = f"Function '{name}' processes {args[0]}"
            else:
                params = ", ".join(args)
                summary = f"Function '{name}' operates on {param_count} parameters: {params}"
        
        return summary
    
    def summarize_class(self, class_info):
        """Generate a summary for a single class"""
        name = class_info['name']
        methods = class_info['methods']
        
        method_count = len(methods)
        
        if method_count == 0:
            summary = f"Class '{name}' is defined but has no methods"
        elif method_count == 1:
            summary = f"Class '{name}' has 1 method: {methods[0]}"
        else:
            summary = f"Class '{name}' has {method_count} methods: {', '.join(methods[:3])}"
            if method_count > 3:
                summary += f" and {method_count - 3} more"
        
        return summary
    
    def determine_purpose(self):
        """Infer the general purpose of the code"""
        imports = self.summary_data['imports']
        functions = self.summary_data['functions']
        classes = self.summary_data['classes']
        
        # Check imports to guess purpose
        purposes = []
        
        # Data science libraries
        if any('pandas' in imp or 'numpy' in imp or 'sklearn' in imp for imp in imports):
            purposes.append("data analysis/machine learning")
        
        # Web frameworks
        if any('flask' in imp or 'django' in imp or 'fastapi' in imp for imp in imports):
            purposes.append("web application")
        
        # File operations
        if any('os' in imp or 'pathlib' in imp or 'shutil' in imp for imp in imports):
            purposes.append("file/system operations")
        
        # Math/calculations
        if any('math' in imp or 'statistics' in imp for imp in imports):
            purposes.append("mathematical calculations")
        
        # Database
        if any('sqlite' in imp or 'mysql' in imp or 'postgres' in imp for imp in imports):
            purposes.append("database operations")
        
        if purposes:
            return f"This code appears to be for {' and '.join(purposes)}"
        else:
            return "This code provides general-purpose functionality"
    
    def generate_full_summary(self):
        """Generate a complete summary of the code"""
        summary_lines = []
        
        # Header
        summary_lines.append("=" * 70)
        summary_lines.append("CODE SUMMARY REPORT")
        summary_lines.append("=" * 70)
        summary_lines.append("")
        
        # Purpose
        summary_lines.append("📋 PURPOSE:")
        summary_lines.append(f"   {self.determine_purpose()}")
        summary_lines.append("")
        
        # Statistics
        num_functions = len(self.summary_data['functions'])
        num_classes = len(self.summary_data['classes'])
        num_imports = len(self.summary_data['imports'])
        
        summary_lines.append("📊 STATISTICS:")
        summary_lines.append(f"   - Functions: {num_functions}")
        summary_lines.append(f"   - Classes: {num_classes}")
        summary_lines.append(f"   - Imports: {num_imports}")
        summary_lines.append("")
        
        # Complexity
        complexity = self.analyze_complexity()
        summary_lines.append("🔍 COMPLEXITY ANALYSIS:")
        summary_lines.append(f"   - Conditional statements (if): {complexity['if_statements']}")
        summary_lines.append(f"   - Loops (for/while): {complexity['loops']}")
        summary_lines.append(f"   - Exception handling (try/except): {complexity['try_except']}")
        summary_lines.append("")
        
        # Imports
        if num_imports > 0:
            summary_lines.append("📦 DEPENDENCIES:")
            for imp in self.summary_data['imports'][:5]:  # Show first 5
                summary_lines.append(f"   - {imp}")
            if num_imports > 5:
                summary_lines.append(f"   ... and {num_imports - 5} more")
            summary_lines.append("")
        
        # Classes
        if num_classes > 0:
            summary_lines.append("🏗️  CLASSES:")
            for cls in self.summary_data['classes']:
                summary_lines.append(f"   • {self.summarize_class(cls)}")
            summary_lines.append("")
        
        # Functions
        if num_functions > 0:
            summary_lines.append("⚙️  FUNCTIONS:")
            for func in self.summary_data['functions']:
                summary_lines.append(f"   • {self.summarize_function(func)}")
            summary_lines.append("")
        
        # Security/Audit Notes
        summary_lines.append("🔒 AUDIT NOTES:")
        audit_notes = self.generate_audit_notes()
        for note in audit_notes:
            summary_lines.append(f"   - {note}")
        summary_lines.append("")
        
        summary_lines.append("=" * 70)
        
        return "\n".join(summary_lines)
    
    def generate_audit_notes(self):
        """Generate security/audit relevant observations"""
        notes = []
        
        # Check for file operations
        imports = self.summary_data['imports']
        
        if any('os' in imp for imp in imports):
            notes.append("Code interacts with the operating system - verify file path handling")
        
        if any('subprocess' in imp or 'os.system' in imp for imp in imports):
            notes.append("⚠️  WARNING: Code executes system commands - requires security review")
        
        if any('pickle' in imp for imp in imports):
            notes.append("⚠️  WARNING: Uses pickle - potential code execution vulnerability")
        
        if any('eval' in self.source_code or 'exec' in self.source_code):
            notes.append("⚠️  CRITICAL: Uses eval/exec - high security risk")
        
        # Check for network operations
        if any('requests' in imp or 'urllib' in imp or 'socket' in imp for imp in imports):
            notes.append("Code makes network requests - verify data validation")
        
        # Check for database operations
        if any('sql' in imp.lower() for imp in imports):
            notes.append("Database operations detected - check for SQL injection prevention")
        
        if not notes:
            notes.append("No obvious security concerns detected in imports")
        
        return notes


# Test the summarizer!
if __name__ == "__main__":
    # Test with a sample program
    sample_program = """
import os
import sqlite3
import hashlib

class UserManager:
    '''Manages user authentication and data'''
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None
    
    def connect(self):
        '''Connect to the database'''
        self.connection = sqlite3.connect(self.db_path)
    
    def hash_password(self, password):
        '''Hash a password for secure storage'''
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username, password):
        '''Create a new user account'''
        hashed = self.hash_password(password)
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO users VALUES (?, ?)", (username, hashed))
        self.connection.commit()

def validate_username(username):
    '''Check if username is valid'''
    if len(username) < 3:
        return False
    if not username.isalnum():
        return False
    return True

def main():
    '''Main entry point'''
    manager = UserManager("users.db")
    manager.connect()
    
    for i in range(10):
        if validate_username(f"user{i}"):
            manager.create_user(f"user{i}", "password123")
"""
    
    print("\n" + "🔍 ANALYZING CODE..." + "\n")
    
    summarizer = CodeSummarizer(sample_program)
    summary = summarizer.generate_full_summary()
    
    print(summary)
    
    # Also save to file
    with open("summary_output.txt", "w") as f:
        f.write(summary)
    
    print("\n✅ Summary saved to 'summary_output.txt'")