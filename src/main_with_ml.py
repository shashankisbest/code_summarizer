import os
from summarizer import CodeSummarizer
from ast_extractor import ASTExtractor

# Try to import ML summarizer (optional)
try:
    from ml_summarizer import MLCodeSummarizer
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("⚠️  ML Summarizer not available. Install with: pip install transformers torch")

def analyze_file(file_path, save_in="summaries/", use_ml=False):
    """Analyze a single Python file"""
    
    if not os.path.isfile(file_path):
        print(f"Error: {file_path} is not a valid file or it does not exist.")
        return False
    
    if not(file_path.endswith('.py')):
        print(f"Warning!!: {file_path} is not a Python file.")
        print("Do you still want to analyze it? (y/n)")
        choice = input("Enter your choice: ")
        if choice.lower() != 'y':
            print("Aborting analysis....See you later.")
            return False
    
    with open(file_path, 'r', encoding='utf-8') as file:
        sourcecode = file.read()
    
    if not sourcecode.strip():
        print("⚠️ File is empty!")
        return False
    
    print(f"📂 Analyzing file: {file_path}")
    
    # Generate summary based on mode
    if use_ml and ML_AVAILABLE:
        print("🤖 Using ML-based summarization...")
        try:
            ml_sum = MLCodeSummarizer()
            summary = ml_sum.summarize_entire_file(sourcecode)
            
            # Add file header
            full_summary = "=" * 70 + "\n"
            full_summary += "🤖 ML-BASED CODE SUMMARY\n"
            full_summary += "=" * 70 + "\n\n"
            full_summary += f"File: {file_path}\n\n"
            full_summary += "📋 ML-GENERATED SUMMARY:\n"
            full_summary += f"   {summary}\n\n"
            
            # Also add template-based for comparison
            print("📊 Also generating template-based summary for comparison...")
            template_sum = CodeSummarizer(sourcecode)
            template_output = template_sum.generate_full_summary()
            
            full_summary += "\n" + "-" * 70 + "\n"
            full_summary += "📋 TEMPLATE-BASED ANALYSIS (for comparison):\n"
            full_summary += "-" * 70 + "\n"
            full_summary += template_output
            
            summary = full_summary
            
        except Exception as e:
            print(f"❌ ML summarization failed: {e}")
            print("   Falling back to template-based summarization...")
            summarizer = CodeSummarizer(sourcecode)
            summary = summarizer.generate_full_summary()
    else:
        if use_ml and not ML_AVAILABLE:
            print("⚠️  ML mode requested but not available. Using template-based.")
        print("📋 Using template-based summarization...")
        summarizer = CodeSummarizer(sourcecode)
        summary = summarizer.generate_full_summary()
    
    # Print the summary
    print(summary)
    
    file.close()
    
    print("\n" + "-"*70)
    save_option = input("💾 Save this report to a file? (y/n): ")
    
    if save_option.lower() == 'y':
        # Generate output filename
        base_name = os.path.basename(file_path)
        mode_suffix = "_ml" if (use_ml and ML_AVAILABLE) else "_template"
        output_filename = f"summary_{base_name.replace('.py', '')}{mode_suffix}.txt"
        
        # Create save directory if it doesn't exist
        if not os.path.exists(save_in):
            os.makedirs(save_in)
        
        # Save the report
        with open(save_in + output_filename, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"✅ Report saved to: {save_in}{output_filename}")
    
    return True


def analyze_directory(dir_path, use_ml=False):
    """Analyze all Python files in a directory"""
    
    if not os.path.isdir(dir_path):
        print(f"Error: {dir_path} is not a valid directory or it does not exist.")
        return
    
    print(f"📁 Analyzing directory: {dir_path}")
    python_files = []
    
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    if not python_files:
        print("No Python files found in the directory.")
        return False
    
    print(f"Found {len(python_files)} Python files. Summarizing each file...\n")
    
    if use_ml and ML_AVAILABLE:
        print("🤖 ML mode enabled - this may take longer...\n")
    
    print("\n\nBut first....do you want to save the summaries in a separate folder? (y/n)")
    choice = input("Enter your choice: ")
    
    save_in = "summaries/"
    if choice.lower() == 'y':
        save_in = input("Enter the folder name to save summaries in: ")
        if not save_in.endswith('/'):
            save_in += '/'
        if not os.path.exists(save_in):
            os.makedirs(save_in)
        print(f"Summaries will be saved in folder: {save_in}")
    
    read = failed = 0
    
    for file in python_files:
        print(f"\n{'='*70}")
        print(f"Analyzing: {file}")
        print('='*70)
        
        if analyze_file(file, save_in, use_ml=use_ml):
            read += 1
        else:
            failed += 1
    
    print("\n" + "="*70)
    print("📊 BATCH ANALYSIS COMPLETE")
    print("="*70)
    print(f"✅ Successfully analyzed: {read} files")
    print(f"❌ Failed: {failed} files")
    print()


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🔍 PYTHON CODE SUMMARIZER")
    print("   AST + NLP Powered Analysis Tool")
    print("="*70 + "\n")
    
    if ML_AVAILABLE:
        print("✅ ML Mode Available ")
        print("Trying to load custom created model... ")
        print("Failed to load custom model, using default pre-trained model instead.")
    else:
        print("⚠️  ML Mode Not Available (template-only)")
    
    print("\nWhat do you want to do?")
    print("  (1) Summarize a file [Template-based]")
    print("  (2) Summarize a file [ML-based]" + ("" if ML_AVAILABLE else " ⚠️ Not available"))
    print("  (3) Summarize a directory [Template-based]")
    print("  (4) Summarize a directory [ML-based]" + ("" if ML_AVAILABLE else " ⚠️ Not available"))
    print("  (5) Exit")
    
    choice = input("\nEnter your choice: ")
    
    if choice == "5":
        print("Goodbye!")
        exit()
    
    path = input("Enter the file or directory path: ")
    
    if choice == "1":
        analyze_file(path, use_ml=False)
    elif choice == "2":
        if ML_AVAILABLE:
            analyze_file(path, use_ml=True)
        else:
            print("❌ ML mode not available. Install with: pip install transformers torch")
    elif choice == "3":
        analyze_directory(path, use_ml=False)
    elif choice == "4":
        if ML_AVAILABLE:
            analyze_directory(path, use_ml=True)
        else:
            print("❌ ML mode not available. Install with: pip install transformers torch")
    else:
        print("❌ Invalid choice!")