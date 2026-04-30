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


def _repair_truncated_json(s: str) -> str:
    """
    Best-effort repair of a truncated JSON string.
    Closes any unclosed strings, arrays, and objects so json.loads
    has a chance of succeeding even when the LLM ran out of output tokens.
    """
    s = s.rstrip()
    if s.endswith("}"):
        return s  # looks complete already
 
    # Walk the string tracking depth and string context,
    # recording the last position we could safely truncate to.
    depth = 0
    in_string = False
    escape_next = False
    last_safe = 0
 
    for i, ch in enumerate(s):
        if escape_next:
            escape_next = False
            continue
        if ch == "\\" and in_string:
            escape_next = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch in "{[":
            depth += 1
        elif ch in "}]":
            depth -= 1
            last_safe = i + 1       # just after a fully-closed structure
        elif ch == "," and depth == 1:
            last_safe = i           # safe to cut here and close the root object
 
    # Truncate to last safe point, remove trailing comma.
    s = s[:last_safe].rstrip().rstrip(",")
 
    # Close any remaining open brackets / braces.
    arr_opens = s.count("[") - s.count("]")
    obj_opens = s.count("{") - s.count("}")
    s += "]" * max(arr_opens, 0)
    s += "}" * max(obj_opens, 0)
    return s
 
 
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
 
        # Strip markdown code fences the model sometimes wraps around JSON.
        clean = re.sub(r"```json|```", "", raw).strip()
 
        # ── Repair pass 1: invalid escape sequences ───────────────────────
        # JSON only allows \", \\, \/, \b, \f, \n, \r, \t, \uXXXX.
        # LLMs often emit bare backslashes inside SVG/LaTeX fields.
        clean = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', clean)
 
        # ── Parse with two fallback repair levels ─────────────────────────
        try:
            data = json.loads(clean)
 
        except json.JSONDecodeError as exc:
            # Repair pass 2: strip any remaining bad escapes more aggressively.
            clean2 = re.sub(r'\\(?!["\\/bfnrtu0-9])', "", clean)
            try:
                data = json.loads(clean2)
 
            except json.JSONDecodeError:
                # Repair pass 3: the output was truncated (unterminated string).
                # Close open structures and retry.
                clean3 = _repair_truncated_json(clean2)
                try:
                    data = json.loads(clean3)
                except json.JSONDecodeError as final_exc:
                    raise RuntimeError(
                        "Could not parse model response as JSON after three repair "
                        f"attempts.\nOriginal error: {exc}\nFinal error: {final_exc}"
                    ) from final_exc
 
        self.paper_title = data.get("title", "Research Paper")
        
        if progress_callback:
            progress_callback(2)
        # Build QA chain with paper title available for context.
        self.qa_chain = build_qa_chain(
            self.vector_store,
            self.api_key,
            QA_PROMPT_TEMPLATE,
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