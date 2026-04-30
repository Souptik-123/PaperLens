# 🔬 PaperLens — Research Paper Explainer AI
### Built with LangChain + Streamlit + Claude (Anthropic)

---

## What It Does

Upload any PDF research paper and get:
- **Technical overview** — abstract, problem, contributions, methodology, results, limitations
- **Architecture diagrams** — AI-generated SVG diagrams of the paper's key components
- **Mathematical equations** — extracted equations rendered with LaTeX
- **Worked examples** — concrete, step-by-step illustrations of techniques
- **Q&A Chat** — RAG-powered chat (FAISS vector store + Claude) for deep questions

---

## Architecture

```
PDF Upload
    │
    ▼
PyPDFLoader (LangChain)
    │  loads pages as Documents
    ▼
RecursiveCharacterTextSplitter
    │  chunk_size=1000, overlap=150
    ▼
HuggingFace Embeddings (all-MiniLM-L6-v2)
    │  384-dim sentence embeddings
    ▼
FAISS Vector Store
    │  MMR retrieval (k=5, fetch_k=10)
    ▼
RetrievalQA Chain (LangChain)          ←─── Claude Sonnet (LLM)
    │  stuff chain type
    ▼
Structured Answer

Parallel:
Full text (60k chars) ──→ Claude Sonnet ──→ Structured JSON
                          (analysis prompt)   (title, equations,
                                               diagrams, examples...)
```

---

## Setup

### 1. Clone / place files

```
paper_explainer/
├── app.py              # Streamlit UI
├── pipeline.py         # LangChain pipeline
├── requirements.txt    # Dependencies
└── README.md
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** First run downloads `all-MiniLM-L6-v2` (~90 MB) for embeddings.

### 3. Get an Anthropic API key

Sign up at https://console.anthropic.com and create an API key (`sk-ant-...`).

### 4. Run the app

```bash
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

---

## Usage

1. Enter your **Anthropic API key** in the sidebar
2. **Upload a PDF** research paper (any domain)
3. Click **Analyze Paper** — analysis takes ~15–30 seconds
4. Browse the tabs:
   - **Overview** — full structured breakdown
   - **Diagrams** — SVG architecture diagrams
   - **Equations** — LaTeX-rendered math
   - **Examples** — worked step-by-step examples
   - **Ask Questions** — RAG-powered Q&A chat

---

## Key LangChain Components

| Component | Usage |
|---|---|
| `PyPDFLoader` | Load PDF pages as LangChain Documents |
| `RecursiveCharacterTextSplitter` | Chunk text with overlap |
| `HuggingFaceEmbeddings` | Embed chunks with sentence-transformers |
| `FAISS` | Vector store for semantic retrieval |
| `RetrievalQA` | RAG chain: retrieve → stuff → generate |
| `ChatAnthropic` | Claude Sonnet LLM for analysis + Q&A |
| `PromptTemplate` | Structured prompts for QA chain |

---

## Requirements

```
streamlit>=1.35.0
langchain>=0.2.0
langchain-anthropic>=0.1.15
langchain-community>=0.2.0
pypdf>=4.2.0
faiss-cpu>=1.8.0
tiktoken>=0.7.0
anthropic>=0.28.0
sentence-transformers>=2.7.0   # for HuggingFaceEmbeddings
```

---

## Customization Tips

- **Change embedding model**: Edit `_make_embeddings()` in `pipeline.py`
- **Adjust chunk size**: Modify `chunk_size` and `chunk_overlap` in `build_vector_store()`
- **Change retrieval strategy**: Switch from `"mmr"` to `"similarity"` in `as_retriever()`
- **Use a different LLM**: Swap `ChatAnthropic` for `ChatOpenAI`, `ChatGroq`, etc.
- **Add memory to chat**: Replace `RetrievalQA` with `ConversationalRetrievalChain`

---

## Troubleshooting

**"sentence_transformers not found"**
```bash
pip install sentence-transformers
```

**"pypdf not found"**
```bash
pip install pypdf
```

**API errors**: Make sure your Anthropic API key is valid and has credits.

**Slow first run**: The embedding model (~90 MB) downloads automatically on first use.
