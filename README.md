# AI-Powered Research Proposal Review Assistant

An AI-powered research proposal analysis application built with **Retrieval-Augmented Generation (RAG)**. The system supports proposal question answering, automated review, and structured scoring through an interactive Streamlit interface.

## Features
- PDF text extraction and cleaning
- 200-word overlapping chunking with 50-word overlap
- 384-dimensional embeddings using `all-MiniLM-L6-v2`
- FAISS `IndexFlatL2` nearest-neighbor retrieval
- Top-3 nearest-chunk retrieval with an L2-distance threshold
- Gemini-powered context-grounded question answering
- Automated proposal review
- Scoring across Novelty, Technical Quality, Methodology, Clarity, and Feasibility
- Retrieved-context transparency and conversation history
- Downloadable review and score outputs

## Technology Stack
**Python · Streamlit · RAG · Sentence Transformers · FAISS · Google Gemini API · PyMuPDF**

## Pipeline
```text
Research Proposal PDF
        ↓
Text Extraction
        ↓
Text Cleaning
        ↓
Overlapping Chunking
        ↓
384-D Embeddings
        ↓
FAISS IndexFlatL2
        ↓
L2 Nearest-Neighbor Search
        ↓
Gemini LLM
        ↓
Q&A / Review / Scoring
```

## Results
The tested proposal workflow processed a **2,703-word proposal into 19 chunks**, generated **384-dimensional embeddings**, and used **top-3 FAISS retrieval** for question answering.

## Setup

```bash
git clone <repository-url>
cd AI-Research-Proposal-Review-Assistant
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file using `.env.example` and add your Gemini API key. **Never commit `.env` or your API key to GitHub.**

Run the application:

```bash
python -m streamlit run app/app.py
```
