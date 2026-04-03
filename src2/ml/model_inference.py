# ml/model_inference.py
"""
ML Model Inference Module - Optimized for CodeParrot
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import warnings
warnings.filterwarnings("ignore")

class MLSummarizer:
    def __init__(self, model_path=None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Force CodeParrot as primary
        model_name = model_path if model_path else "codeparrot/codeparrot-small"
        
        print(f"   Using device: {self.device}")
        print(f"   Loading: {model_name}")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                trust_remote_code=False
            )
            
            # Add padding token if missing
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                trust_remote_code=False
            )
            
            self.model.to(self.device)
            self.model.eval()
            self.model_name = model_name
            print(f"   ✅ Successfully loaded: {model_name}")
            
        except Exception as e:
            print(f"   ❌ Failed to load: {e}")
            self.model = None
            self.tokenizer = None
    
    def generate(self, input_text, max_length=150):
        """
        Generate completion using CodeParrot
        """
        if self.model is None:
            return "ML model not available"
        
        try:
            # CodeParrot needs a clear prompt that asks for completion
            prompt = f"""Below is a Python code description. Complete the sentence to describe what this code does.

Code info: {input_text}

This code"""
            
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
                    max_new_tokens=max_length,
                    min_new_tokens=30,
                    num_beams=4,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode and extract only the completion part
            full_output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract after "This code"
            if "This code" in full_output:
                summary = "This code" + full_output.split("This code")[-1]
            else:
                summary = full_output
            
            # Clean up
            summary = summary.strip()
            
            # Ensure it's a complete sentence
            if summary and summary[-1] not in '.!?':
                summary += '.'
            
            # Limit length
            if len(summary) > 300:
                summary = summary[:300] + '...'
            
            return summary if len(summary) > 20 else "This code implements various Python functions and classes."
            
        except Exception as e:
            return f"Generation error: {str(e)[:100]}"
    
    def is_available(self):
        return self.model is not None