# AST-Based Code Summarization Tool

---

Overview
This project is a hybrid system that combines **Compiler Design (AST analysis)** with **Machine Learning (code summarization)**.

Instead of directly feeding raw code into a model, the system first extracts structural information using AST and then generates summaries and audit insights.

---

Key Idea
Traditional approach:
Code → Model → Output

My approach:
Code → AST → Structured Analysis → Model → Output

---

Features
- AST-based structural analysis
- Semantic understanding of code
- Code summarization
- Security audit notes

---
Quick Start

```bash
cd src
python main_with_ml.py
```

---

USER MANUAL

## 1. Setup

### Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

---


## 2. How It Works

1. Input source code
2. AST extraction
3. AST traversal (functions, classes, imports)
4. Semantic analysis
5. Structured representation
6. Model generates:
   - Summary
   - Security notes

---

## 3. Running the System

```bash
cd src
python main_with_ml.py
```

---

## 4. Output

- Program summary
- Component breakdown
- Security audit notes

---

Future Enhancements

- Support more languages
- Improve vulnerability detection

---

Final Note

This is not just a summarizer —  
it is a **structured code understanding system** combining **compiler theory and AI**.
