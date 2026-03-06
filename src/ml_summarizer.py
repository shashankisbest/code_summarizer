from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch
from ast_extractor import ASTExtractor #!basic requirement

class MLCodeSummarizer:
    """
    Uses pre-trained transformer models to generate intelligent code summaries.
    This is the NLP component of the AST + NLP project.
    """
    
    def __init__(self, model_name="Salesforce/codet5-small"):
        """
        Initialize the ML summarizer with a pre-trained model.
        
        Models we can use:
        - "Salesforce/codet5-small" (recommended - fast, good quality)
        - "Salesforce/codet5-base" (larger, better quality, slower)
        - "microsoft/codebert-base" (alternative)
        """
        print(f"🤖 Loading ML model: {model_name}...")
        print("   (This may take a minute on first run...)")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            self.model_name = model_name
            print("✅ Model loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print("   Falling back to simpler model...")
            # Fallback to a guaranteed-to-work model
            self.model_name = "t5-small"
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
    
    def summarize_code_snippet(self, code_text, max_length=50):
        """
        Generate a summary for a code snippet using the ML model.
        
        Args:
            code_text: The source code to summarize
            max_length: Maximum length of generated summary
            
        Returns:
            Generated summary string
        """
        try:
            # Prepare input for the model
            # For CodeT5, we can add a task prefix
            if "codet5" in self.model_name.lower():
                input_text = f"summarize: {code_text}"
            else:
                input_text = code_text
            
            # Tokenize input
            inputs = self.tokenizer(
                input_text,
                return_tensors="pt",
                max_length=512,
                truncation=True,
                padding=True
            )
            
            # Generate summary
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    min_length=10,
                    num_beams=4,  # Beam search for better quality
                    early_stopping=True,
                    no_repeat_ngram_size=2  # Avoid repetition
                )
            
            # Decode the output
            summary = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return summary.strip()
            
        except Exception as e:
            return f"[ML Error: {str(e)}]"
    
    def summarize_function(self, func_code, func_name=None):
        """
        Summarize a single function using ML.
        
        Args:
            func_code: The function's source code
            func_name: Optional function name for context
            
        Returns:
            ML-generated summary
        """
        # Limit code length to avoid token limits
        if len(func_code) > 2000:
            func_code = func_code[:2000] + "..."
        
        summary = self.summarize_code_snippet(func_code, max_length=60)
        
        if func_name and func_name not in summary:
            summary = f"Function '{func_name}': {summary}"
        
        return summary
    
    def summarize_class(self, class_code, class_name=None):
        """
        Summarize a class using ML.
        
        Args:
            class_code: The class's source code
            class_name: Optional class name for context
            
        Returns:
            ML-generated summary
        """
        # Limit code length
        if len(class_code) > 2000:
            class_code = class_code[:2000] + "..."
        
        summary = self.summarize_code_snippet(class_code, max_length=60)
        
        if class_name and class_name not in summary:
            summary = f"Class '{class_name}': {summary}"
        
        return summary
    
    def summarize_entire_file(self, source_code):
        """
        Generate a high-level summary of the entire file.
        
        Args:
            source_code: Complete source code
            
        Returns:
            File-level summary
        """
        # For entire file, we want a shorter, high-level summary
        # Take only the first 1500 characters for context
        if len(source_code) > 1500:
            source_code = source_code[:1500] + "..."
        
        summary = self.summarize_code_snippet(source_code, max_length=80)
        return summary


# Simple test
if __name__ == "__main__":
    print("\n" + "="*70)
    print("Testing ML Code Summarizer")
    print("="*70 + "\n")
    
    #^ sample Test code
    test_code = """
def calculate_circle_area(radius):
    '''Calculate the area of a circle'''
    pi = 3.14159
    area = pi * radius * radius
    return area

def calculate_rectangle_area(length, width):
    '''Calculate area of rectangle'''
    return length * width
"""
    
    # Initialize ML summarizer
    ml_sum = MLCodeSummarizer()
    
    print("\n📝 Test Code:")
    print(test_code)
    
    print("\n🤖 ML-Generated Summary:")
    summary = ml_sum.summarize_entire_file(test_code)
    print(f"   {summary}")
    
    print("\n" + "="*70)
    print("✅ Test Complete!")


