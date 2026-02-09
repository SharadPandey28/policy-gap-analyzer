# Cybersecurity Policy Gap Analyzer (Offline AI + NLP)

An offline cybersecurity compliance analysis tool that evaluates organizational policy documents against security frameworks (e.g., NIST CSF) and automatically:

* Detects missing controls
* Identifies weak coverage
* Calculates compliance score
* Generates gap reports
* Produces an AI-revised policy
* Provides a remediation roadmap

The system runs **fully offline** using:

* Local NLP matching
* Ollama (phi3) local LLM
* Streamlit dashboard

No cloud APIs or internet dependency required.

---

# Features

✅ Upload PDF or TXT policy
✅ Offline gap detection using NLP
✅ Compliance percentage scoring
✅ Visual dashboard (charts + tables)
✅ AI-generated improved policy
✅ Remediation roadmap
✅ CSV download of gap report
✅ Fully local execution

---

# System Requirements

* Python 3.10+
* Git
* Ollama installed locally
* 4GB+ RAM recommended

---

# Installation & Dependencies (B)

## Step 1 — Clone repository

```bash
git clone https://github.com/<your-username>/policy-gap-analyzer.git
cd policy-gap-analyzer
```

## Step 2 — Create virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

## Step 4 — Install Ollama model

```bash
ollama pull phi3:mini
```

---

# How to Run (A)

## Option 1 — CLI mode

Run:

```bash
python run.py
```

Outputs:

```
gap report
revised policy
roadmap
```

---

## Option 2 — Streamlit Dashboard (Recommended)

Run:

```bash
streamlit run frontend.py
```

Open browser:

```
http://localhost:8501
```

Steps:

1. Upload policy file (.pdf or .txt)
2. Click Analyze
3. View dashboard + charts + downloads

---

# Logic & Workflow Explanation (C)

The system follows a multi-stage pipeline:

---

## Step 1 — Policy Upload

User uploads policy document (PDF/TXT).

---

## Step 2 — Text Extraction

* PDF → PyPDF reader
* TXT → direct read

Converted to plain text.

---

## Step 3 — Text Segmentation

Policy is split into sentence-level segments.

Example:

```
Systems are patched regularly.
User accounts use unique IDs.
```

---

## Step 4 — Clause Preprocessing

Security controls (NIST/CIS) are stored in JSON with:

* requirement text
* keywords

Each clause is normalized:

* lowercase
* remove punctuation
* clean whitespace

---

## Step 5 — Offline NLP Matching

Each policy segment is compared against each control using:

### Keyword overlap scoring

```
matched keywords / total keywords
```

If ≥ 50% → Covered

Else:
→ Partial or Missing

This avoids heavy ML and keeps execution fast.

---

## Step 6 — Gap Report Generation

Produces structured output:

```
{
  clause_id,
  title,
  coverage,
  score,
  matched_text
}
```

---

## Step 7 — Compliance Calculation

```
Compliance = covered_controls / total_controls
```

Displayed in dashboard.

---

## Step 8 — Policy Revision (LLM)

Missing controls are passed to local Ollama model:

```
phi3:mini
```

LLM:

* adds missing sections
* improves wording
* generates roadmap

All done offline.

---

## Step 9 — Visualization

Streamlit displays:

* Pie chart
* Bar chart
* Control table
* Revised policy
* Roadmap
* CSV downloads

---

# Project Structure

```
policy-gap-analyzer/
│
├── frontend.py        → Streamlit dashboard
├── run.py             → CLI runner
├── requirements.txt
├── README.md
│
├── app/
│   ├── service.py     → pipeline orchestration
│   ├── nlp/           → text matching
│   ├── loaders/       → file readers
│   ├── reporting/     → gap reports
│   ├── remediation/   → policy rewrite
│   └── llm/           → ollama client
│
├── data/              → control definitions
└── outputs/
```

---

# Limitations (D)

Current version has:

* Keyword-based matching only (no deep semantic similarity)
* Basic sentence segmentation
* LLM responses may vary
* Designed for small/medium policies (not 1000+ pages)
* Framework coverage limited to provided JSON controls

---

# Future Improvements

Planned enhancements:

* Vector embeddings (FAISS)
* Better semantic search
* Multi-framework support
* Domain heatmap visualization
* Batch policy upload
* PDF report export
* Web deployment
* Fine-tuned local LLM
* Advanced risk scoring

---

# Why Offline?

Advantages:

* No data leakage
* No cloud dependency
* Faster inference
* Suitable for sensitive policies
* Works in restricted networks

---

# Tech Stack

* Python
* Streamlit
* Ollama (phi3)
* Scikit-learn
* PyPDF
* Pandas / Plotly


