from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM, pipeline
import torch
import warnings
warnings.filterwarnings("ignore")

class MLCodeSummarizer:
    """
    Uses pre-trained transformer models to generate intelligent code summaries.
    """
    
    def __init__(self, model_name="codeparrot/codeparrot-small"):
        """
        Initialize the ML summarizer with a pre-trained model.
        
        Models we can use:
        - "codeparrot/codeparrot-small" (recommended - stable, good for code)
        - "microsoft/CodeGPT-small-py" (alternative)
        - "Salesforce/codet5-small" (if it works)
        """
        print(f"🤖 Loading ML model: {model_name}...")
        print("   (This may take a minute on first run...)")
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Try multiple models in order of preference
        models_to_try = [
            "codeparrot/codeparrot-small",  # First try CodeParrot
            "microsoft/CodeGPT-small-py",   # Then try CodeGPT
            "gpt2",                          # Then try GPT-2 (works reliably)
            "Salesforce/codet5-small"        # Finally try CodeT5
        ]
        
        # Remove duplicates
        models_to_try = list(dict.fromkeys(models_to_try))
        
        self.model = None
        self.tokenizer = None
        self.is_causal_lm = True  # Most code models are causal LMs
        
        for attempt_model in models_to_try:
            try:
                print(f"   Attempting to load: {attempt_model}")
                
                if "codet5" in attempt_model.lower():
                    # CodeT5 is seq2seq
                    self.tokenizer = AutoTokenizer.from_pretrained(attempt_model)
                    self.model = AutoModelForSeq2SeqLM.from_pretrained(attempt_model)
                    self.is_causal_lm = False
                else:
                    # Most code models are causal LMs
                    self.tokenizer = AutoTokenizer.from_pretrained(attempt_model)
                    self.model = AutoModelForCausalLM.from_pretrained(attempt_model)
                    self.is_causal_lm = True
                
                # Add padding token if it doesn't exist
                if self.tokenizer.pad_token is None:
                    self.tokenizer.pad_token = self.tokenizer.eos_token
                
                self.model.to(self.device)
                self.model_name = attempt_model
                print(f"✅ Successfully loaded: {attempt_model}")
                break
                
            except Exception as e:
                print(f"   ⚠️ Could not load {attempt_model}: {str(e)[:50]}...")
                continue
        
        if self.model is None:
            raise RuntimeError("❌ Failed to load any model!")
    
    def summarize_code_snippet(self, code_text, max_length=100):
        """
        Generate a summary for a code snippet.
        """
        try:
            # Clean and prepare the code
            code_text = code_text.strip()
            if not code_text:
                return "Empty code snippet"
            
            # Truncate very long code
            if len(code_text) > 500:
                code_text = code_text[:500] + "..."
            
            # Create a prompt for summarization
            prompt = f"Here's what this code does:\n{code_text}\n\nSummary: This code"
            
            # Tokenize
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                max_length=512,
                truncation=True,
                padding=True
            ).to(self.device)
            
            # Generate summary
            with torch.no_grad():
                if self.is_causal_lm:
                    outputs = self.model.generate(
                        **inputs,
                        max_length=len(inputs['input_ids'][0]) + max_length,
                        min_length=10,
                        num_beams=3,
                        early_stopping=True,
                        no_repeat_ngram_size=2,
                        pad_token_id=self.tokenizer.pad_token_id,
                        eos_token_id=self.tokenizer.eos_token_id
                    )
                else:
                    outputs = self.model.generate(
                        **inputs,
                        max_length=max_length,
                        min_length=10,
                        num_beams=3,
                        early_stopping=True,
                        no_repeat_ngram_size=2
                    )
            
            # Decode and clean
            summary = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract just the summary part
            if "Summary: This code" in summary:
                summary = summary.split("Summary: This code")[-1].strip()
            elif "Summary:" in summary:
                summary = summary.split("Summary:")[-1].strip()
            
            # Clean up
            summary = summary.replace("This code", "").strip()
            if summary and summary[0].islower():
                summary = summary[0].upper() + summary[1:]
            
            return summary if summary else "Code snippet that performs a specific function"
            
        except Exception as e:
            return f"[Summary: {str(e)}]"
    
    def summarize_function(self, func_code, func_name=None):
        """
        Summarize a function.
        """
        # Extract function signature and docstring if present
        lines = func_code.split('\n')
        signature = lines[0] if lines else ""
        
        # Look for docstring
        docstring = ""
        if len(lines) > 1 and '"""' in lines[1]:
            # Simple docstring extraction
            for i, line in enumerate(lines[1:], 1):
                docstring += line + "\n"
                if '"""' in line and i > 1:
                    break
        
        # Create summary input
        if docstring:
            input_text = f"{signature}\n{docstring}"
        else:
            input_text = func_code[:300]  # First 300 chars
        
        summary = self.summarize_code_snippet(input_text, max_length=50)
        
        if func_name:
            return f"Function '{func_name}': {summary}"
        return summary
    
    def summarize_class(self, class_code, class_name=None):
        """
        Summarize a class.
        """
        # Extract class signature and methods
        lines = class_code.split('\n')
        signature = lines[0] if lines else ""
        
        # Find methods
        methods = []
        for line in lines[:10]:  # Check first 10 lines
            if 'def ' in line:
                methods.append(line.strip())
        
        # Create summary input
        input_text = signature
        if methods:
            input_text += "\nMethods: " + ", ".join(methods[:3])
        
        summary = self.summarize_code_snippet(input_text, max_length=50)
        
        if class_name:
            return f"Class '{class_name}': {summary}"
        return summary
    
    def summarize_entire_file(self, source_code):
        """
        Generate a high-level summary of the entire file.
        """
        lines = source_code.split('\n')
        
        # Extract key components
        imports = [l for l in lines if l.strip().startswith(('import ', 'from '))]
        classes = [l for l in lines if 'class ' in l]
        functions = [l for l in lines if 'def ' in l and not l.strip().startswith('def __')]
        
        # Create a structured summary input
        summary_parts = []
        
        if imports:
            summary_parts.append(f"Imports: {len(imports)} modules")
        
        if classes:
            class_names = [c.split('class ')[1].split('(')[0].split(':')[0].strip() for c in classes[:3]]
            summary_parts.append(f"Classes: {', '.join(class_names)}")
        
        if functions:
            func_names = [f.split('def ')[1].split('(')[0].strip() for f in functions[:5]]
            summary_parts.append(f"Functions: {', '.join(func_names)}")
        
        # Look for a main block
        has_main = any('if __name__ == "__main__"' in line for line in lines)
        if has_main:
            summary_parts.append("Has main entry point")
        
        # Combine for summary
        context = " | ".join(summary_parts)
        
        if not context:
            # If no structure found, use first few lines
            context = source_code[:300]
        
        summary = self.summarize_code_snippet(context, max_length=80)
        
        return summary


# Simple test
if __name__ == "__main__":
    print("\n" + "="*70)
    print("Testing ML Code Summarizer")
    print("="*70 + "\n")
    
    test_code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# Example usage
num = int(input("Enter a number: "))
print("Factorial:", factorial(num))
"""
    
    try:
        ml_sum = MLCodeSummarizer()
        
        print("\n📝 Test Code:")
        print(test_code)
        
        print("\n🤖 ML-Generated Summary:")
        summary = ml_sum.summarize_entire_file(test_code)
        print(f"   {summary}")
        
        print("\n🔍 Function Summary:")
        func_summary = ml_sum.summarize_function(test_code, "factorial")
        print(f"   {func_summary}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*70)
    print("✅ Test Complete!")