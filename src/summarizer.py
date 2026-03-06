import ast
from ast_extractor import ASTExtractor


class CodeSummarizer:


    def __init__(self,sourcecode):

        self.extractor = ASTExtractor(sourcecode)
        self.summary_data = self.extractor.get_summary_data()
        
        self.sourcecode = sourcecode
        self.tree = ast.parse(sourcecode)
        
    

    def analyze_complexity(self):
        #& this code doesn't mean time complexity
        #& this just records how complex your code is


        information = {
            'if_statements': 0,
            'loops': 0,
            'try_except': 0,
        }

        for node in ast.walk(self.tree):
            if isinstance(node,ast.If):
                information['if_statements'] += 1

            if isinstance(node,(ast.For,ast.While)):
                information['loops'] += 1

            if isinstance(node,ast.Try):
                information['try_except'] += 1

        return information
    

    def summarize_function(self,func_info):
        #todo summary for a single function

        name = func_info['name']
        args = func_info['args']
        docstring = func_info['docstring']

        summary = f"the function {name}"
        if docstring:
            summary = summary + f" : {docstring}"

        else:
            if len(args) == 0:
                summary = summary + f" operates on no parameters. "

            else: summary = summary + f" operates on {args}"

        return summary
    


    def summarize_class(self,class_info):

        #todo same but for classes

        name = class_info['name']
        methods = class_info['methods']

        if len(methods) == 0:
            return f"the class {name} is there but it does not contain any methods in it"
        
        else:
            return f"the class{name} exists with {len(methods)} methods inside it named {methods}"
    




    def determine_purpose(self):
        
        imports = self.summary_data["imports"]
        functions = self.summary_data["functions"]
        classes = self.summary_data["classes"]

        # todo lets find out all the purposes of the code
        purposes = list()

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
                return f"This code is mostly be going to be used for :{'and'.join(purposes)}"
            else: return f"Unable to find a match for the purpose...maybe this code is used for something new."



    def generate_audit_notes(self):
        notes=[]

        imports = self.summary_data['imports']

        #! file operations
        if any('os' in imp for imp in imports):
            notes.append("Code interacts with the operating system - verify file path handling")

        if any('subprocess' in imp or 'os.system' in imp for imp in imports):
            notes.append("⚠️  WARNING: Code executes system commands - requires security review")
        
        if any('pickle' in imp for imp in imports):
            notes.append("⚠️  WARNING: Uses pickle - potential code execution vulnerability")
        
        if 'eval' in self.sourcecode or 'exec' in self.sourcecode:
            notes.append("⚠️  CRITICAL: Uses eval/exec - high security risk")
        
        #! Check for network operations
        if any('requests' in imp or 'urllib' in imp or 'socket' in imp for imp in imports):
            notes.append("Code makes network requests - verify data validation")
        
        #! Check for database operations
        if any('sql' in imp.lower() for imp in imports):
            notes.append("Database operations detected - check for SQL injection prevention")
        
        if not notes:
            notes.append("No obvious security concerns detected in imports")
        
        return notes


#^-----------------------------------------------
    def generate_full_summary(self):

        #^^ finally generating full summary for the code


        #summary could be big hence storing it in the form of list
        summary_lines = []


        summary_lines.append("CODE SUMMARY REPORT")
        summary_lines.append("=" * 70)
        summary_lines.append("\n\n")        

        # Purpose
        summary_lines.append("---->PURPOSE<----")
        summary_lines.append(f"   {self.determine_purpose()}")
        summary_lines.append("\n\n")

        # Statistics
        num_functions = len(self.summary_data['functions'])
        num_classes = len(self.summary_data['classes'])
        num_imports = len(self.summary_data['imports'])
        
        summary_lines.append("---->STATISTICS<----")
        summary_lines.append(f"   - Functions: {num_functions}")
        summary_lines.append(f"   - Classes: {num_classes}")
        summary_lines.append(f"   - Imports: {num_imports}")
        summary_lines.append("\n\n")
        
        # Complexity
        complexity = self.analyze_complexity()
        summary_lines.append("---->COMPLEXITY ANALYSIS<----")
        summary_lines.append(f"   - Conditional statements (if): {complexity['if_statements']}")
        summary_lines.append(f"   - Loops (for/while): {complexity['loops']}")
        summary_lines.append(f"   - Exception handling (try/except): {complexity['try_except']}")
        summary_lines.append("\n\n")

        # Imports
        if num_imports > 0:
            summary_lines.append("---->DEPENDENCIES<----")
            for imp in self.summary_data['imports']:  
                summary_lines.append(f"   - {imp}")

            summary_lines.append("\n\n")       

        if num_classes>0:
            summary_lines.append("---->CLASSES<----")

            for clas in self.summary_data['classes']:
                summary_lines.append(f"   • {self.summarize_class(clas)}") 
            summary_lines.append("\n\n")            


        # Functions
        if num_functions > 0:
            summary_lines.append("---->FUNCTIONS<----")
            for func in self.summary_data['functions']:
                summary_lines.append(f"   • {self.summarize_function(func)}")
            summary_lines.append("\n\n")
        

        # Security/Audit Notes
        summary_lines.append("---->🔒 AUDIT NOTES<----")
        audit_notes = self.generate_audit_notes()
        for note in audit_notes:
            summary_lines.append(f"   - {note}")
        summary_lines.append("\n\n")
        
        summary_lines.append("=" * 70)


        # and then print them like a paragraph 
        return "\n".join(summary_lines)




#testing the summarizer
if __name__ == "__main__":

#  again sample code
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
    
    print("\n" + "ANALYZING CODE..." + "\n")
    
    summarizer = CodeSummarizer(sample_program)
    summary = summarizer.generate_full_summary()
    
    
    # Also save to file
    with open("summary_output.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    
    print("\nSummary saved to 'summary_output.txt'")