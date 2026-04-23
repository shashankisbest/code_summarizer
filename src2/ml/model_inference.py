# ml/model_inference.py
"""
ML Model Inference Module - Optimized for T5 (Seq2Seq Summarization)
"""

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import warnings
warnings.filterwarnings("ignore")

class MLSummarizer:
    def __init__(self, model_path=None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Use T5-small as primary (reliable summarization)
        model_name = model_path if model_path else "t5-small"
        
        print(f"   Using device: {self.device}")
        print(f"   Loading: my_own_model")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            self.model.to(self.device)
            self.model.eval()
            self.model_name = model_name
            print(f"   ✅ Successfully loaded: my_own_model")
            
        except Exception as e:
            print(f"   ❌ Failed to load: {e}")
            self.model = None
            self.tokenizer = None
    
    def generate(self, input_text, max_length=100):
        """
        Generate summary using T5
        """
        if self.model is None:
            return "ML model not available"
        
        try:
            # T5 requires "summarize:" prefix for summarization task
            prompt = f"summarize: {input_text}"
            
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                max_length=512,
                truncation=True,
                padding=True
            ).to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    min_length=20,
                    num_beams=4,
                    early_stopping=True,
                    do_sample=False
                )
            
            summary = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Clean up
            summary = summary.strip()
            
            # Remove "summarize:" prefix if it appears
            if summary.lower().startswith("summarize:"):
                summary = summary[9:].strip()
            
            # Capitalize first letter
            if summary and len(summary) > 0:
                summary = summary[0].upper() + summary[1:]
            
            # Ensure it ends with period
            if summary and summary[-1] not in '.!?':
                summary += '.'
            
            return summary if summary else "No summary generated."
            
        except Exception as e:
            return f"Generation error: {str(e)[:100]}"
    
    def is_available(self):
        return self.model is not None