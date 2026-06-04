# 🎯 Personalized AI Resume Scorer & Analyzer Dashboard

An advanced **Multimodal AI-powered Applicant Tracking System (ATS)** built to critically evaluate resume document formatting layouts alongside industry experience metrics using the updated **Google GenAI SDK** and **Gemini 2.5 Flash**.

## 🛠️ The Tech Stack Architecture
- **Frontend/Dashboard:** Streamlit (Python-Native Reactive Data Framework)
- **AI Core:** Google GenAI Engine (`gemini-2.5-flash` model)
- **Document Processing:** PyMuPDF (`fitz`) for low-latency visual page encoding
- **Memory Management:** Streamlit Session State RAM Caching

## 🚀 Key Production Features
- **Multimodal Visual Processing:** Instead of parsing plain, lossy text strings, the system analyzes font hierarchies, spacing grids, and alignment layouts visually.
- **Strict JSON Output Controls:** Configured API endpoints with a structural MIME-type mask to guarantee consistent data objects.
- **Persistent Cache Tracking:** Implemented session states to preserve analytical scoring objects during UI interactions.
- **In-Memory Document Exporting:** Generates real-time report summaries dynamically over local RAM buffers.

## 📦 Local Configuration Guide

1. Clone the project:
   ```bash
   git clone [https://github.com/your-username/ai-resume-analyzer.git](https://github.com/tejakhileshkonda-ops/ai-resume-analyzer.git)