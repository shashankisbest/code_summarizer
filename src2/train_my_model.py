# train_my_model.py
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainer, Seq2SeqTrainingArguments
from datasets import Dataset
import json

# Load your dataset
print("📚 Loading dataset...")
with open("ast_summary_dataset.jsonl", "r") as f:
    data = [json.loads(line) for line in f]

dataset = Dataset.from_list(data)
dataset = dataset.train_test_split(test_size=0.1)
print(f"✅ Loaded {len(data)} examples")

# Load model
print("🤖 Loading model...")
model_name = "t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Tokenize
def preprocess(examples):
    inputs = tokenizer(examples["input"], max_length=128, truncation=True, padding="max_length")
    targets = tokenizer(examples["output"], max_length=64, truncation=True, padding="max_length")
    inputs["labels"] = targets["input_ids"]
    return inputs

print("🔄 Tokenizing...")
tokenized_dataset = dataset.map(preprocess, batched=True)

# Training arguments
training_args = Seq2SeqTrainingArguments(
    output_dir="./my_own_model",
    num_train_epochs=5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    learning_rate=3e-4,
    save_strategy="epoch",
    eval_strategy="epoch",
    predict_with_generate=True,
    logging_steps=50,
    report_to="none",
)

# FIXED: Removed 'tokenizer' parameter
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    # tokenizer=tokenizer,  # REMOVE THIS LINE
)

print("🏋️ Starting training...")
trainer.train()

# Save
trainer.save_model("./my_own_model")
tokenizer.save_pretrained("./my_own_model")
print("✅ Your OWN model saved to ./my_own_model")