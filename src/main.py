import os
from summarizer import CodeSummarizer
from ast_extractor import ASTExtractor

def analyze_file(file_path, save_in = "summaries/"):
    print("Debug1")
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
    
    print(f"Summarizing file: {file_path}")
    summarizer = CodeSummarizer(sourcecode)
    summary = summarizer.generate_full_summary()


    print(summary)
    
    file.close()
    
    print("\n" + "-"*70)
    save_option = input("💾 Save this report to a file? (y/n): ")
    
    if save_option.lower() == 'y':
        # Generate output filename
        base_name = os.path.basename(file_path)
        output_filename = f"summary_{base_name.replace('.py', '.txt')}"
        
        # Save the report
        with open(save_in+output_filename, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"✅ Report saved to: {output_filename}")
    
    return True

#-----------------------------------------------------------------------------------------


def analyze_directory(dir_path):
    print("debug2")
    if not os.path.isdir(dir_path):
        print(f"Error: {dir_path} is not a valid directory or it does not exist.")
        return
    
    print(f"Analyzing directory: {dir_path}")

    python_files = []

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))

    if not python_files:
        print("No Python files found in the directory.")
        return False
    
    print(f"Found {len(python_files)} Python files. Summarizing each file...\n")

    print("\n\nBut first....do you want to save the summaries in a separate folder? (y/n)")
    choice = input("Enter your choice: ")
    
    save_in = "summaries/"
    if choice.lower() == 'y':
        save_in = input("Enter the folder name to save summaries in: ")
        if not os.path.exists(save_in):
            os.makedirs(save_in)
        print(f"Summaries will be saved in folder: {save_in}")




    read = failed = 0

    for file in python_files:
        print(f"\n{'='*70}")
        print(f"Analyzing: {file}")
        print('='*70)

        if analyze_file(file, save_in):  #^using upper function
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
    print("Welcome to the Python Code Summarizer!")
    print("What do you want to do? (1) Summarize a file, (2) Summarize a directory, (3) Exit")

    choice = input("Enter your choice: ")

    if choice == "3":
        print("Goodbye!")
        exit()


    path = input("Enter the file or directory path: ")

    if choice == "1":
        analyze_file(path)

    elif choice == "2":
        analyze_directory(path)