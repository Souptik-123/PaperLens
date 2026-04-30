import json
import re
from typing import Callable, Optional

from core.loader import load_pdf
from core.splitter import split_docs
from core.embeddings import make_embeddings
from core.vectorstore import build_vectorstore

from chains.explain_chain import get_explain_chain
from chains.qa_chain import build_qa_chain

from utils.prompts import ANALYSIS_SYSTEM_PROMPT, QA_PROMPT_TEMPLATE


class PaperPipeline:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.docs = []
        self.full_text = ""
        self.vector_store = None
        self.qa_chain = None
        self.paper_title = ""

    # ── Stage 1
    def load_pdf(self, pdf_path: str):
        self.docs, self.full_text = load_pdf(pdf_path)

    # ── Stage 2
    def build_vector_store(self):
        chunks = split_docs(self.docs)
        embeddings = make_embeddings(self.api_key)
        self.vector_store = build_vectorstore(chunks, embeddings)

    # ── Stage 3
    def generate_explanation(self, progress_callback: Optional[Callable] = None):
        if progress_callback:
            progress_callback(0)

        explain = get_explain_chain(self.api_key, ANALYSIS_SYSTEM_PROMPT)
        raw = explain(self.full_text)

        if progress_callback:
            progress_callback(1)

        clean = re.sub(r"```json|```", "", raw).strip()
        data = json.loads(clean)

        self.paper_title = data.get("title", "Research Paper")

        if progress_callback:
            progress_callback(2)

        self.qa_chain = build_qa_chain(
            self.vector_store,
            self.api_key,
            QA_PROMPT_TEMPLATE
        )

        return data

    # ── Stage 4
    def answer_question(self, question: str):
        if self.qa_chain:
            try:
                result = self.qa_chain.invoke({"query": question})
                return result.get("result", str(result))
            except Exception:
                pass

        return "QA system not ready."