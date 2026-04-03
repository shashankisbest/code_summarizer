# main.py
"""
Hybrid Code Summarizer - Main Entry Point
Combines AST analysis with ML for comprehensive code understanding
"""

import sys
import os
import argparse
from pathlib import Path

# Add src2 to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from summarizer.hybrid_summarizer import HybridSummarizer

def print_banner():
    """Print application banner"""
    print("\n" + "="*70)
    print("🔍 HYBRID CODE SUMMARIZER")
    print("   AST Analysis + ML Generation")
    print("="*70 + "\n")

def load_code_from_file(filepath):
    """Load code from file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None

def main():
    """Main entry point"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='AST-NLP Code Summarizer')
    parser.add_argument('file', nargs='?', help='Python file to analyze')
    parser.add_argument('--mode', choices=['template', 'ml', 'custom', 'hybrid'], 
                        default='hybrid', help='Summarization mode')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--format', choices=['text', 'json', 'markdown'], 
                        default='text', help='Output format')
    args = parser.parse_args()
    
    print_banner()
    
    # Initialize ML model ONLY if not in template mode
    ml_model = None
    if args.mode != 'template':
        try:
            from ml.model_inference import MLSummarizer
            print("🤖 Initializing Hybrid Summarizer...")
            ml_model = MLSummarizer()
            if ml_model.is_available():
                print("✅ ML Model loaded successfully!")
            else:
                print("⚠️ ML Model not available, using template mode")
                args.mode = 'template'
        except Exception as e:
            print(f"⚠️ Could not load ML model: {e}")
            print("   Using template mode...")
            args.mode = 'template'
    else:
        print("🤖 Using Template-Only Mode (ML disabled)")
    
    summarizer = HybridSummarizer(ml_model=ml_model)
    
    # If file provided as argument, analyze it directly
    if args.file:
        if os.path.isfile(args.file):
            code = load_code_from_file(args.file)
            if code:
                use_ml = (args.mode != 'template')
                report = summarizer.summarize(code, use_ml=use_ml)
                print(report)
                
                if args.output:
                    with open(args.output, 'w', encoding='utf-8') as f:
                        f.write(report)
                    print(f"\n✅ Report saved to: {args.output}")
            return
    
    # Interactive mode
    while True:
        print("\nWhat do you want to do?")
        print("  (1) Summarize a file [Template-based]")
        print("  (2) Summarize a file [ML-based]")
        print("  (3) Summarize a directory [Template-based]")
        print("  (4) Summarize a directory [ML-based]")
        print("  (5) Exit")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            use_ml = False
            filepath = input("Enter file path: ").strip()
            code = load_code_from_file(filepath)
            if code:
                print("\n" + "="*70)
                report = summarizer.summarize(code, use_ml=use_ml)
                print(report)
                
                save = input("\n💾 Save report to file? (y/n): ").lower()
                if save == 'y':
                    output_file = filepath.replace('.py', '_report.txt')
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(report)
                    print(f"✅ Report saved to: {output_file}")
        
        elif choice == '2':
            use_ml = True
            filepath = input("Enter file path: ").strip()
            code = load_code_from_file(filepath)
            if code:
                print("\n" + "="*70)
                report = summarizer.summarize(code, use_ml=use_ml)
                print(report)
                
                save = input("\n💾 Save report to file? (y/n): ").lower()
                if save == 'y':
                    output_file = filepath.replace('.py', '_report.txt')
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(report)
                    print(f"✅ Report saved to: {output_file}")
        
        elif choice == '3':
            use_ml = False
            dirpath = input("Enter directory path: ").strip()
            if os.path.isdir(dirpath):
                py_files = list(Path(dirpath).glob("*.py"))
                if not py_files:
                    print("❌ No Python files found in directory")
                    continue
                
                print(f"\n📁 Found {len(py_files)} Python files")
                for py_file in py_files[:10]:
                    print(f"\n📄 Analyzing: {py_file.name}")
                    code = load_code_from_file(py_file)
                    if code:
                        report = summarizer.summarize(code, use_ml=use_ml)
                        print(report[:500] + "...\n")
            else:
                print("❌ Invalid directory path")
        
        elif choice == '4':
            use_ml = True
            dirpath = input("Enter directory path: ").strip()
            if os.path.isdir(dirpath):
                py_files = list(Path(dirpath).glob("*.py"))
                if not py_files:
                    print("❌ No Python files found in directory")
                    continue
                
                print(f"\n📁 Found {len(py_files)} Python files")
                for py_file in py_files[:10]:
                    print(f"\n📄 Analyzing: {py_file.name}")
                    code = load_code_from_file(py_file)
                    if code:
                        report = summarizer.summarize(code, use_ml=use_ml)
                        print(report[:500] + "...\n")
            else:
                print("❌ Invalid directory path")
        
        elif choice == '5':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()