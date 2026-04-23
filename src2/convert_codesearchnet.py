# convert_codesearchnet.py
import ast
import json
from datasets import load_dataset

def extract_ast_features(code_string):
    """Safely extract basic features from a code string."""
    features = {
        "functions": [],
        "classes": [],
        "imports": [],
        "complexity": "unknown"
    }
    try:
        tree = ast.parse(code_string)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                features["functions"].append(node.name)
            elif isinstance(node, ast.ClassDef):
                features["classes"].append(node.name)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                features["imports"].append("import")
        # Approximate complexity
        features["complexity"] = "high" if len(features["functions"]) > 5 else "low"
    except SyntaxError:
        pass
    return features

def format_ast_input(features):
    """Convert extracted features to a text string for model input."""
    return (f"Functions: {', '.join(features['functions'][:5]) or 'none'} | "
            f"Classes: {', '.join(features['classes'][:3]) or 'none'} | "
            f"Imports: {len(features['imports'])} modules | "
            f"Complexity: {features['complexity']}")

def main():
    print("Loading CodeSearchNet Python dataset...")
    dataset = load_dataset("code_search_net", "python", split="train", trust_remote_code=False)

    print(f"Processing {len(dataset)} examples...")
    converted_data = []
    
    # FIXED: Use correct field names for CodeSearchNet
    for i, example in enumerate(dataset):
        if i >= 1000:  # Change this for more data
            break
            
        # CodeSearchNet uses 'func_code_string' not 'code'
        # and 'func_documentation_string' not 'docstring'
        code = example.get("func_code_string", "")
        docstring = example.get("func_documentation_string", "")
        
        # Also try alternative field names if above don't work
        if not code:
            code = example.get("code", "")
        if not docstring:
            docstring = example.get("docstring", "")
        
        if not docstring or len(docstring) < 10:
            continue
            
        features = extract_ast_features(code)
        ast_text = format_ast_input(features)
        
        converted_data.append({
            "input": ast_text,
            "output": docstring.strip().replace("\n", " ")
        })
        
        if (i + 1) % 100 == 0:
            print(f"Processed {i+1} examples...")

    # Save to file
    output_path = "ast_summary_dataset.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for entry in converted_data:
            f.write(json.dumps(entry) + "\n")
    
    print(f"\n✅ Dataset created! {len(converted_data)} examples saved to {output_path}")
    
    # Show sample
    if converted_data:
        print("\n📋 Sample entry:")
        print(json.dumps(converted_data[0], indent=2))

if __name__ == "__main__":
    main()