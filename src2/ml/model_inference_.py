# ml/model_inference.py
"""
ML Model Inference Module - Optimized for Custom Model + CodeParrot
"""

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
import warnings
import os
warnings.filterwarnings("ignore")

class MLSummarizer:
    def __init__(self, model_path=None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # List of models to try in order (YOUR CUSTOM MODEL FIRST!)
        models_to_try = [
            # "./my_own_model",              # 🔥 my trained model (seq2seq)
            "codeparrot/codeparrot-small", # CodeParrot fallback (causal)
            "t5-small",                    # Final fallback
        ]
        
        # If user specified a specific model, try that first
        if model_path:
            models_to_try.insert(0, model_path)
        
        self.model = None
        self.tokenizer = None
        self.model_type = None
        self.model_name = None
        
        print(f"   Using device: {self.device}")
        
        for model_name in models_to_try:
            try:
                print(f"   Attempting: {model_name}")
                
                # Check if it's your custom model (seq2seq)
                if model_name == "./my_own_model" or os.path.isdir(model_name):
                    # Your custom model is seq2seq (T5-based)
                    self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                    self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
                    self.model_type = "seq2seq"
                    
                elif "codeparrot" in model_name.lower():
                    # CodeParrot is causal
                    self.tokenizer = AutoTokenizer.from_pretrained(
                        model_name,
                        trust_remote_code=False
                    )
                    if self.tokenizer.pad_token is None:
                        self.tokenizer.pad_token = self.tokenizer.eos_token
                    self.model = AutoModelForCausalLM.from_pretrained(
                        model_name,
                        trust_remote_code=False
                    )
                    self.model_type = "causal"
                    
                else:
                    # T5 and other seq2seq models
                    self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                    self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
                    self.model_type = "seq2seq"
                
                self.model.to(self.device)
                self.model.eval()
                self.model_name = model_name
                print(f"   ✅ Successfully loaded: {model_name}")
                print(f"   📊 Model type: {self.model_type}")
                break
                
            except Exception as e:
                print(f"   ⚠️ Failed to load {model_name}: {str(e)[:80]}...")
                continue
        
        if self.model is None:
            print("   ⚠️ No ML model loaded. Using template-only mode.")
    
    def generate(self, input_text, max_length=150):
        """
        Generate summary using loaded model
        """
        if self.model is None:
            return "ML model not available"
        
        try:
            # Different handling based on model type
            if self.model_type == "causal":
                # CodeParrot-style completion
                prompt = f"""Below is a Python code description. Complete the sentence.

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
                
                full_output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                
                if "This code" in full_output:
                    summary = "This code" + full_output.split("This code")[-1]
                else:
                    summary = full_output
                    
            else:
                # Seq2seq models (YOUR custom model, T5, etc.)
                # Your model was trained on "input -> output" directly
                inputs = self.tokenizer(
                    input_text,
                    return_tensors="pt",
                    max_length=128,
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
            
            # Ensure it's a complete sentence
            if summary and summary[-1] not in '.!?':
                summary += '.'
            
            # Limit length
            if len(summary) > 300:
                summary = summary[:300] + '...'
            
            # Fallback if too short
            if len(summary) < 20:
                return "This code implements various Python functions and classes."
            
            return summary
            
        except Exception as e:
            return f"Generation error: {str(e)[:100]}"
    
    def is_available(self):
        return self.model is not None