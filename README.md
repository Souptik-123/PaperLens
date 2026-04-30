# 🔬 PaperLens — Research Paper Explainer AI
###Built with LangChain + Streamlit + OpenAI
> Upload any PDF research paper and get a full technical breakdown — architecture diagrams, mathematical equations, worked examples, and an AI tutor ready to answer your questions.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-0.1%2B-1C3C3C?logo=chainlink&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-412991?logo=openai&logoColor=white)
![FAISS](https://img.shields.io/badge/Vector%20Store-FAISS-009688)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [File Reference](#file-reference)
- [Known Issues & Fixes](#known-issues--fixes)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

**PaperLens** is a Streamlit web application that transforms dense academic PDF papers into interactive, structured knowledge. Powered by LangChain, OpenAI's GPT-4o-mini, and FAISS vector search, it automatically extracts:

- A structured technical overview (abstract, problem, contributions, methodology, results, limitations)
- SVG architecture/pipeline diagrams generated from the paper's content
- LaTeX-rendered mathematical equations with variable definitions and significance
- Worked examples with pseudocode
- A retrieval-augmented Q&A chat tutor scoped to the paper

---

## Features

| Feature | Description |
|---|---|
| 📋 **Technical Overview** | Auto-extracted title, authors, venue, abstract, problem statement, contributions, methodology, results, and limitations |
| 📊 **Architecture Diagrams** | 2–3 inline SVG diagrams representing key components, pipelines, or flows |
| ➗ **Math Equations** | 3–5 key equations in LaTeX with raw form, variable definitions, and significance |
| 💡 **Worked Examples** | Concrete step-by-step walkthroughs with optional Python pseudocode |
| 💬 **RAG Q&A Chat** | MMR-based retrieval-augmented chat tutor with suggested starter questions |
| 🏷️ **Tagging** | Auto-generated domain/topic tags with colour coding |
| 🌑 **Dark UI** | Academic dark-mode aesthetic built with custom Streamlit CSS |

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        app.py                           │
│                   (Streamlit UI)                        │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                     pipeline.py                         │
│                   (PaperPipeline)                       │
│                                                         │
│  Stage 1: load_pdf()       → loader.py                  │
│  Stage 2: build_vector_store() → splitter.py            │
│                               embeddings.py             │
│                               vectorstore.py (FAISS)    │
│  Stage 3: generate_explanation() → explain_chain.py     │
│                                    prompts.py           │
│  Stage 4: answer_question()  → qa_chain.py (RAG)        │
└─────────────────────────────────────────────────────────┘
```

**Data flow:**

```
PDF Upload → PyPDFLoader → RecursiveCharacterTextSplitter
          → OpenAI Embeddings → FAISS Vector Store
          → GPT-4o-mini (full text) → Structured JSON Analysis
          → RetrievalQA (MMR search) → Chat Answers
```

---

## Project Structure

```
paperlens/
│
├── app.py                  # Streamlit UI — sidebar, tabs, chat interface
├── pipeline.py             # PaperPipeline orchestrator (4-stage pipeline)
├── config.py               # Global constants (model, chunk size, top-k)
|           
|── core/
├──── loader.py               # PyPDFLoader wrapper → (docs, full_text)
├──── splitter.py             # RecursiveCharacterTextSplitter wrapper
├──── embeddings.py           # OpenAIEmbeddings factory (text-embedding-3-small)
├──── vectorstore.py          # FAISS builder + retriever factory
|        
│── chains/
├──── explain_chain.py        # GPT-4o-mini chain → structured JSON analysis
├──── qa_chain.py             # RetrievalQA chain with MMR retriever
|
|── utils           
├──── prompts.py              # ANALYSIS_SYSTEM_PROMPT + QA_PROMPT_TEMPLATE
│
└── README.md
```

---

## Installation

### Prerequisites

- Python 3.9 or higher
- An [OpenAI API key](https://platform.openai.com/api-keys)

### 1. Clone the repository

```bash
git clone https://github.com/Souptik-123/PaperLens.git
cd PaperLens
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt`**

```
streamlit>=1.30.0
langchain>=0.1.0
langchain-openai>=0.1.0
langchain-community>=0.0.20
faiss-cpu>=1.7.4
pypdf>=3.0.0
openai>=1.0.0
```

### 4. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## Usage

1. **Enter your OpenAI API key** in the sidebar (`sk-...`).
2. **Upload a PDF** research paper using the file uploader.
3. Click **🚀 Analyze Paper** — the pipeline runs through 4 stages:
   - Reading & chunking the PDF
   - Building the FAISS vector store
   - Generating the full structured analysis via GPT-4o-mini
   - Initialising the RAG Q&A chain
4. Explore the **5 tabs**:
   - **📋 Overview** — metadata, tags, abstract, methodology, results, limitations
   - **📊 Diagrams** — rendered SVG architecture diagrams
   - **➗ Equations** — LaTeX equations with explanations
   - **💡 Examples** — worked examples with pseudocode
   - **💬 Ask Questions** — chat with suggested starter questions
5. Click **🔄 New Paper** in the sidebar to reset and analyze another paper.

---

## Configuration

Edit `config.py` to tune pipeline behaviour:

```python
OPENAI_MODEL   = "gpt-5.4"   # Model used for analysis and QA
TEMPERATURE    = 0.3              # Generation temperature
CHUNK_SIZE     = 1000              # Characters per text chunk
CHUNK_OVERLAP  = 150             # Overlap between chunks
TOP_K          = 4                # Default retriever top-k (overridden to 5 in QA chain with MMR)
```

**Explain chain** (`explain_chain.py`): uses `temperature=0.2`, `max_completion_tokens=16000`, truncates input to maximum characters needed.

**QA chain** (`qa_chain.py`): uses MMR retrieval with `k=5`, `fetch_k=10`, `temperature=0.3`, `max_tokens=2000`.

---

## How It Works

### Stage 1 — PDF Loading (`loader.py`)

Uses LangChain's `PyPDFLoader` to extract text page by page. Returns both the list of `Document` objects (for chunking) and a single concatenated `full_text` string (for the explain chain).

### Stage 2 — Chunking & Embedding (`splitter.py`, `embeddings.py`, `vectorstore.py`)

Documents are split with `RecursiveCharacterTextSplitter` using separators `["\n\n", "\n", ". ", " ", ""]`. Chunks are embedded with OpenAI's `text-embedding-3-small` model and indexed in a FAISS vector store for fast similarity search.

### Stage 3 — Structured Analysis (`explain_chain.py`, `prompts.py`)

The full paper text (up to 60,000 characters) is sent to GPT-4o-mini with `ANALYSIS_SYSTEM_PROMPT`, which instructs the model to return a strict JSON object containing title, authors, venue, abstract, problem, contributions, methodology, results, limitations, tags, SVG diagrams, LaTeX equations, worked examples, and suggested Q&A questions.

The JSON is parsed and stored in `st.session_state.paper_data`.

### Stage 4 — Retrieval-Augmented Q&A (`qa_chain.py`)

A `RetrievalQA` chain is built with an MMR retriever (fetches 10 candidates, returns top 5 diverse chunks). User questions are answered using the retrieved paper excerpts as context, with `QA_PROMPT_TEMPLATE` guiding technically precise, equation-aware responses.

---

## File Reference

### `app.py`
Main Streamlit application. Handles page config, custom CSS, sidebar (API key input, file upload, pipeline trigger), and the 5-tab main content area. Stores pipeline instance, paper data, and chat history in `st.session_state`.

### `pipeline.py`
`PaperPipeline` class encapsulating the 4-stage processing pipeline. Holds state across stages (`docs`, `full_text`, `vector_store`, `qa_chain`, `paper_title`). Accepts an optional `progress_callback` for live UI updates during analysis.

### `config.py`
Central configuration constants. Change model, temperature, chunk sizes, and retrieval `k` here without touching pipeline logic.

### `loader.py`
Thin wrapper around `PyPDFLoader`. Returns `(docs, full_text)` — `docs` is the list of LangChain `Document` objects; `full_text` is the full concatenated string.

### `splitter.py`
Wraps `RecursiveCharacterTextSplitter`. Takes a list of `Document` objects and returns a list of smaller `Document` chunks ready for embedding.

### `embeddings.py`
Factory function returning an `OpenAIEmbeddings` instance using the `text-embedding-3-small` model.

### `vectorstore.py`
Builds a FAISS index from document chunks and embeddings. `get_retriever()` returns a simple similarity retriever; the QA chain uses its own MMR retriever configured inline.

### `explain_chain.py`
Builds a callable that sends the paper's full text to GPT-4o-mini with the analysis system prompt and returns the raw JSON string response.

### `qa_chain.py`
Builds a `RetrievalQA` chain using the FAISS vector store, a custom `PromptTemplate`, and an MMR-configured retriever. Accepts `paper_title` to optionally personalise the chain context.

### `prompts.py`
Contains two prompts:
- `ANALYSIS_SYSTEM_PROMPT` — strict JSON schema instruction for the explain chain
- `QA_PROMPT_TEMPLATE` — retrieval-augmented answer prompt with context and question slots

---

## Known Issues & Fixes

### Equations not rendering in Q&A chat

**Symptom:** LaTeX like `\[ h_t = f(h_{t-1}, x_t) \]` appears as raw text in the chat panel.

**Cause:** AI responses were injected into a raw HTML `<div>` via `unsafe_allow_html=True`, bypassing Streamlit's MathJax renderer.

**Fix:** Replace the AI message block in `app.py` with native `st.markdown()`:

```python
# Before (broken)
content = msg["content"].replace("\n", "<br>")
st.markdown(f"<div class='chat-ai'>{content}</div>", unsafe_allow_html=True)

# After (fixed)
st.markdown("<div class='avatar-ai'>🔬 PaperLens AI</div>", unsafe_allow_html=True)
with st.container():
    st.markdown(msg["content"])   # LaTeX renders correctly here
```

### Papers with scanned/image-only pages

`PyPDFLoader` extracts text only. Scanned PDFs without an embedded text layer will produce empty or garbled output. Consider integrating an OCR step (e.g., `pytesseract` or `pymupdf` with OCR) for such documents.

### Very long papers (> 60,000 characters)

The explain chain truncates input to 60,000 characters. For book-length papers, consider summarising sections before passing to the analysis chain, or splitting the analysis across multiple calls.

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

Please open an issue first for major changes.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

<div align="center">
  Built with ❤️ using <a href="https://streamlit.io">Streamlit</a> · <a href="https://python.langchain.com">LangChain</a> · <a href="https://openai.com">OpenAI</a>
</div>