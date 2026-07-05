# 🎯 Enterprise RAG-Based AI Resume Analyzer

An advanced, production-grade Applicant Tracking System (ATS) evaluation engine built using a **Retrieval-Augmented Generation (RAG)** pipeline. Instead of feeding unoptimized blocks or lossy strings to a Large Language Model, this platform converts documents into vectors, indexes them locally using **FAISS**, and runs a semantic similarity search against targeted job descriptions before generating deterministic evaluation metrics using the **Google GenAI SDK (Gemini 2.5 Flash)**.

---

## 🛠️ Tech Stack & Architecture

- **Frontend / Core UI:** Streamlit (Python-native reactive framework)
- **Vector Database:** FAISS-CPU (Facebook AI Similarity Search for high-speed vector lookup)
- **Embedding Generation:** Sentence Transformers (`all-MiniLM-L6-v2`)
- **Orchestration Layer:** Traditional RAG (Extract ➔ Chunk ➔ Embed ➔ Match ➔ Ground ➔ Generate)
- **LLM Core Core Engine:** Google GenAI Engine (`gemini-2.5-flash` model)
- **Document Processing:** PyMuPDF (`fitz`) for rapid memory-buffered PDF parsing
- **Configuration Management:** Python-Dotenv

---

## 🚀 Key Features

* **Semantic RAG Pipeline:** Segments multi-page resume payloads into chunks and selects the top $K$ contextually matching fragments related to a specific Job Description, eliminating LLM context window clutter.
* **Local In-Memory Vector Store:** Leverages FAISS for low-latency mathematical indexing and semantic matching.
* **Deterministic Structured JSON Output:** Utilizes strict server-side MIME-type constraints (`application/json`) to eliminate raw text parsing instabilities.
* **Persistent Application Memory:** Implements performance-efficient state tracking across user actions through local RAM serialization via `st.session_state`.
* **Instant Document Exporting:** Compiles analytical suitability telemetry and matrix reviews into dynamic local text reports.

---

## 📦 Local Installation Guide

### 1. Project Replication
Clone this repository to your computer and navigate into its workspace:
```bash
git clone [https://github.com/tejakhileshkonda-ops/ai-resume-analyzer.git](https://github.com/tejakhileshkonda-ops/ai-resume-analyzer.git)
cd ai-resume-analyzer