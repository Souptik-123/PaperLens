import streamlit as st


# ── Page config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="PaperLens · Research Paper Explainer",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Dark, academic-lab aesthetic */
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Source Sans Pro', sans-serif;
}

/* Hide default Streamlit header padding */
.block-container { padding-top: 1.5rem !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0f1117;
    border-right: 1px solid #1e2235;
}
section[data-testid="stSidebar"] * { color: #c8cad4 !important; }
section[data-testid="stSidebar"] .stButton button {
    background: #1a1e2e !important;
    border: 1px solid #2a2f45 !important;
    color: #c8cad4 !important;
    width: 100%;
}
section[data-testid="stSidebar"] .stButton button:hover {
    border-color: #4ade80 !important;
    color: #4ade80 !important;
}

/* Main background */
.stApp { background: #0d0f14; }

/* Headings */
h1, h2, h3 { font-family: 'Lora', serif !important; font-weight: 400 !important; }

/* Cards */
.paper-card {
    background: #13161e;
    border: 1px solid #1e2235;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}

.section-label {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #555c72;
    margin-bottom: 0.5rem;
}

.tag-pill {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 99px;
    font-size: 0.75rem;
    font-weight: 600;
    margin: 2px;
}

.accent-text { color: #4ade80; }
.muted-text  { color: #8b90a0; font-size: 0.875rem; line-height: 1.7; }

/* Equation box */
.eq-box {
    background: #0d0f14;
    border: 1px solid #1e2235;
    border-left: 3px solid #fbbf24;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    margin: 0.75rem 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.875rem;
    color: #fbbf24;
    overflow-x: auto;
}

/* Code block */
.code-box {
    background: #0a0c11;
    border: 1px solid #1e2235;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #a8b1c8;
    overflow-x: auto;
    white-space: pre;
}

/* Chat messages */
.chat-user {
    background: #0f1929;
    border: 1px solid #1a3a5c;
    border-radius: 12px 12px 4px 12px;
    padding: 0.875rem 1.1rem;
    margin: 0.5rem 0;
    color: #c8d8f0;
    font-size: 0.9rem;
    line-height: 1.65;
}

.chat-ai {
    background: #13161e;
    border: 1px solid #1e2235;
    border-radius: 12px 12px 12px 4px;
    padding: 0.875rem 1.1rem;
    margin: 0.5rem 0;
    color: #c8cad4;
    font-size: 0.9rem;
    line-height: 1.65;
}

.avatar-ai   { color: #4ade80; font-weight: 700; font-size: 0.78rem; margin-bottom: 4px; }
.avatar-user { color: #38bdf8; font-weight: 700; font-size: 0.78rem; margin-bottom: 4px; }

/* Metric cards */
.metric-row {
    display: flex;
    gap: 12px;
    margin-bottom: 1rem;
}
.metric-box {
    flex: 1;
    background: #13161e;
    border: 1px solid #1e2235;
    border-radius: 10px;
    padding: 0.875rem;
    text-align: center;
}
.metric-val { font-size: 1.6rem; font-weight: 600; color: #e8eaf0; }
.metric-lbl { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.07em; color: #555c72; }

/* Diagram SVG container */
.svg-wrap {
    background: #0a0c11;
    border: 1px solid #1e2235;
    border-radius: 10px;
    padding: 1.25rem;
    overflow-x: auto;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    background: #13161e;
    border-radius: 10px;
    padding: 4px;
    gap: 2px;
    border: 1px solid #1e2235;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: #8b90a0 !important;
    font-weight: 500;
    padding: 8px 16px;
}
.stTabs [aria-selected="true"] {
    background: #1a1e2e !important;
    color: #4ade80 !important;
}

/* Input fields */
.stTextInput input, .stTextArea textarea {
    background: #13161e !important;
    border: 1px solid #2a2f45 !important;
    border-radius: 8px !important;
    color: #e8eaf0 !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #4ade80 !important;
}

/* Primary button */
.stButton button[kind="primary"] {
    background: #4ade80 !important;
    color: #0d0f14 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
}

/* File uploader */
.stFileUploader {
    background: #13161e !important;
    border: 1.5px dashed #2a2f45 !important;
    border-radius: 12px !important;
}

/* Divider */
hr { border-color: #1e2235 !important; }

/* Spinner */
.stSpinner > div { border-top-color: #4ade80 !important; }

/* Success / info boxes */
.stSuccess { background: rgba(74,222,128,0.08) !important; border-color: rgba(74,222,128,0.25) !important; }
.stInfo    { background: rgba(56,189,248,0.08) !important; border-color: rgba(56,189,248,0.25) !important; }
.stWarning { background: rgba(251,191,36,0.08) !important; border-color: rgba(251,191,36,0.25) !important; }
.stError   { background: rgba(251,113,133,0.08) !important; border-color: rgba(251,113,133,0.25) !important; }
</style>
""", unsafe_allow_html=True)

# ── Imports ──────────────────────────────────────────────────────────────────
import os
import tempfile
from pipeline import PaperPipeline

# ── Session state defaults ───────────────────────────────────────────────────
if "api_key"       not in st.session_state: st.session_state.api_key       = ""
if "pipeline"      not in st.session_state: st.session_state.pipeline      = None
if "paper_data"    not in st.session_state: st.session_state.paper_data    = None
if "chat_history"  not in st.session_state: st.session_state.chat_history  = []
if "paper_ready"   not in st.session_state: st.session_state.paper_ready   = False

# ════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🔬 PaperLens")
    st.markdown("<div style='color:#555c72;font-size:.8rem;margin-bottom:1rem'>Research Paper Explainer AI</div>", unsafe_allow_html=True)
    st.divider()

    # API Key
    st.markdown("**OpenAI API Key**")
    api_key_input = st.text_input(
        "API Key",
        value=st.session_state.api_key,
        type="password",
        placeholder="sk-ant-api03-...",
        label_visibility="collapsed",
    )
    if api_key_input:
        st.session_state.api_key = api_key_input
        os.environ["OPENAI_API_KEY"] = api_key_input

    st.divider()

    # Upload
    st.markdown("**Upload Research Paper**")
    uploaded_file = st.file_uploader(
        "PDF upload",
        type=["pdf"],
        label_visibility="collapsed",
        help="Upload a PDF research paper",
    )

    if uploaded_file and st.session_state.api_key:
        if st.button("🚀 Analyze Paper", type="primary", use_container_width=True):
            with st.spinner(""):
                progress_placeholder = st.empty()
                steps = [
                    "📄 Reading PDF...",
                    "🧠 Extracting concepts...",
                    "📐 Building vector store...",
                    "🔬 Generating explanation...",
                    "📊 Creating diagrams...",
                    "➗ Extracting equations...",
                    "💡 Building examples...",
                    "✅ Ready!",
                ]
                import time

                def update_progress(step_idx):
                    progress_placeholder.markdown(
                        f"<div style='color:#4ade80;font-size:.85rem'>{steps[step_idx]}</div>",
                        unsafe_allow_html=True,
                    )

                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name

                try:
                   
                    api_key=st.session_state.api_key
                    pipeline=PaperPipeline(api_key)
                    update_progress(0)
                    pipeline.load_pdf(tmp_path)
 
                    # FIX: Stage 2 — build vector store via the pipeline instance
                    update_progress(2)
                    pipeline.build_vector_store()
 
                    # FIX: Stage 3 — generate explanation via the pipeline instance
                    update_progress(3)
                    paper_data = pipeline.generate_explanation(
                        progress_callback=lambda i: update_progress(min(i + 3, len(steps) - 1))
                    )
                    st.session_state.pipeline   = pipeline
                    st.session_state.paper_data = paper_data
                    st.session_state.chat_history = []
                    st.session_state.paper_ready  = True

                    progress_placeholder.markdown(
                        "<div style='color:#4ade80;font-size:.85rem'>✅ Paper ready!</div>",
                        unsafe_allow_html=True,
                    )
                except Exception as e:
                    st.error(f"Error: {e}")
                finally:
                    os.unlink(tmp_path)

    elif uploaded_file and not st.session_state.api_key:
        st.warning("Enter your API key first.")

    st.divider()

    if st.session_state.paper_ready:
        p = st.session_state.paper_data
        st.markdown(f"**📄 Loaded**")
        st.markdown(f"<div style='font-size:.8rem;color:#8b90a0;line-height:1.5'>{p.get('title','—')}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:.72rem;color:#555c72;margin-top:4px'>{p.get('authors','')}</div>", unsafe_allow_html=True)
        st.divider()
        if st.button("🔄 New Paper", use_container_width=True):
            st.session_state.pipeline     = None
            st.session_state.paper_data   = None
            st.session_state.chat_history = []
            st.session_state.paper_ready  = False
            st.rerun()

    st.markdown(
        "<div style='color:#333a50;font-size:.7rem;margin-top:2rem'>Built with LangChain + Streamlit</div>",
        unsafe_allow_html=True,
    )

# ════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ════════════════════════════════════════════════════════════════════════════
if not st.session_state.paper_ready:
    # ── Landing ──────────────────────────────────────────────────────────
    st.markdown("""
    <div style='text-align:center;padding:3rem 0 1rem'>
        <div style='font-size:3rem;margin-bottom:1rem'>🔬</div>
        <h1 style='font-family:Lora,serif;font-size:2.5rem;font-weight:400;color:#e8eaf0;margin-bottom:.75rem'>
            Research Paper Explainer
        </h1>
        <p style='font-size:1.05rem;color:#8b90a0;max-width:560px;margin:0 auto;line-height:1.7'>
            Upload any PDF research paper and get a full technical breakdown —
            architecture diagrams, mathematical equations, worked examples,
            and an AI tutor ready to answer your questions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    features = [
        ("📋", "Technical\nOverview"),
        ("📊", "Architecture\nDiagrams"),
        ("➗", "Math\nEquations"),
        ("💡", "Worked\nExamples"),
        ("💬", "Q&A\nChat"),
    ]
    for col, (icon, label) in zip([col1, col2, col3, col4, col5], features):
        with col:
            st.markdown(f"""
            <div style='text-align:center;background:#13161e;border:1px solid #1e2235;
                        border-radius:10px;padding:1.25rem .5rem'>
                <div style='font-size:1.5rem'>{icon}</div>
                <div style='font-size:.75rem;color:#8b90a0;margin-top:.5rem;white-space:pre-line'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("👈 Add your OpenAI API key and upload a PDF in the sidebar to get started.")

else:
    # ── Paper loaded: show tabs ───────────────────────────────────────────
    p = st.session_state.paper_data

    tabs = st.tabs(["📋 Overview", "📊 Diagrams", "➗ Equations", "💡 Examples", "💬 Ask Questions"])

    # ────────────────────────────────────────────────────────────────────
    # TAB 1 — OVERVIEW
    # ────────────────────────────────────────────────────────────────────
    with tabs[0]:
        st.markdown(f"# {p.get('title', 'Untitled')}")
        st.markdown(f"<div style='color:#8b90a0;font-size:.9rem;margin-bottom:1.5rem'>{p.get('authors','')} · {p.get('venue','')}</div>", unsafe_allow_html=True)

        # Tags
        tag_colors = {
            "green":  "#0a1f12", "sky":   "#071825",
            "amber":  "#1f1400", "violet":"#150f28", "rose":"#200a10",
        }
        tag_text = {
            "green": "#4ade80", "sky": "#38bdf8",
            "amber": "#fbbf24", "violet": "#a78bfa", "rose": "#fb7185",
        }
        tags_html = ""
        for tag, color in (p.get("tags") or []):
            bg = tag_colors.get(color, "#13161e")
            tc = tag_text.get(color, "#8b90a0")
            tags_html += f"<span class='tag-pill' style='background:{bg};color:{tc};border:1px solid {tc}33'>{tag}</span>"
        st.markdown(tags_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Metrics
        cols = st.columns(4)
        metrics = [
            ("Year",    p.get("year",    "—")),
            ("Pages",   p.get("pages",   "—")),
            ("Equations", str(len(p.get("equations", [])))),
            ("Examples",  str(len(p.get("examples",  [])))),
        ]
        for col, (lbl, val) in zip(cols, metrics):
            with col:
                st.markdown(f"""
                <div class='metric-box'>
                    <div class='metric-val'>{val}</div>
                    <div class='metric-lbl'>{lbl}</div>
                </div>""", unsafe_allow_html=True)

        st.divider()

        # Abstract
        st.markdown("### Abstract")
        st.markdown(f"<div class='muted-text'>{p.get('abstract','')}</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Problem
        st.markdown("### Problem Statement")
        st.markdown(f"<div class='muted-text'>{p.get('problem','')}</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Contributions
        st.markdown("### Key Contributions")
        for i, c in enumerate(p.get("contributions", []), 1):
            st.markdown(f"""
            <div style='display:flex;gap:10px;margin-bottom:.6rem'>
                <span style='color:#4ade80;font-weight:700;flex-shrink:0'>{i}.</span>
                <span class='muted-text'>{c}</span>
            </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Methodology
        st.markdown("### Methodology")
        for para in p.get("methodology", "").split("\n\n"):
            if para.strip():
                st.markdown(f"<div class='muted-text' style='margin-bottom:.75rem'>{para.strip()}</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Results
        st.markdown("### Results & Findings")
        st.markdown(f"<div class='muted-text'>{p.get('results','')}</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Limitations
        st.markdown("### Limitations")
        for lim in p.get("limitations", []):
            st.markdown(f"<div style='display:flex;gap:8px;margin-bottom:.5rem'><span style='color:#fb7185;flex-shrink:0'>⚠</span><span class='muted-text'>{lim}</span></div>", unsafe_allow_html=True)

    # ────────────────────────────────────────────────────────────────────
    # TAB 2 — DIAGRAMS
    # ────────────────────────────────────────────────────────────────────
    with tabs[1]:
        st.markdown("## Architecture Diagrams")
        st.markdown("<div class='muted-text' style='margin-bottom:1.5rem'>Visual representations of key components, pipelines, and architectures from the paper.</div>", unsafe_allow_html=True)

        diagrams = p.get("diagrams", [])
        if diagrams:
            for d in diagrams:
                with st.container():
                    col_title, col_badge = st.columns([4, 1])
                    with col_title:
                        st.markdown(f"#### {d.get('title','Diagram')}")
                        st.markdown(f"<div class='muted-text'>{d.get('description','')}</div>", unsafe_allow_html=True)
                    with col_badge:
                        st.markdown(f"<div style='background:rgba(74,222,128,.1);border:1px solid rgba(74,222,128,.25);color:#4ade80;border-radius:99px;padding:4px 12px;font-size:.72rem;font-weight:700;text-align:center;margin-top:.5rem'>{d.get('type','Diagram')}</div>", unsafe_allow_html=True)

                    st.markdown(f"<div class='svg-wrap'>{d.get('svg','')}</div>", unsafe_allow_html=True)
                    st.caption(d.get("caption", ""))
                    st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.info("No diagrams were generated for this paper.")

    # ────────────────────────────────────────────────────────────────────
    # TAB 3 — EQUATIONS
    # ────────────────────────────────────────────────────────────────────
    with tabs[2]:
        st.markdown("## Mathematical Equations")
        st.markdown("<div class='muted-text' style='margin-bottom:1.5rem'>Core mathematical formulations extracted and explained from the paper.</div>", unsafe_allow_html=True)

        equations = p.get("equations", [])
        if equations:
            for i, eq in enumerate(equations, 1):
                with st.expander(f"**Eq. {i} — {eq.get('title','Equation')}**", expanded=(i == 1)):
                    st.markdown(f"<div class='muted-text' style='margin-bottom:.75rem'>{eq.get('description','')}</div>", unsafe_allow_html=True)

                    # LaTeX equation
                    latex = eq.get("latex", "")
                    if latex:
                        st.latex(latex)

                    # Raw form
                    st.markdown(f"<div class='eq-box'>{eq.get('raw_form', latex)}</div>", unsafe_allow_html=True)

                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown("**Variables**")
                        st.markdown(f"<div class='muted-text'>{eq.get('variables','')}</div>", unsafe_allow_html=True)
                    with col_b:
                        st.markdown("**Significance**")
                        st.markdown(f"<div class='muted-text'>{eq.get('significance','')}</div>", unsafe_allow_html=True)
        else:
            st.info("No equations were extracted for this paper.")

    # ────────────────────────────────────────────────────────────────────
    # TAB 4 — EXAMPLES
    # ────────────────────────────────────────────────────────────────────
    with tabs[3]:
        st.markdown("## Worked Examples")
        st.markdown("<div class='muted-text' style='margin-bottom:1.5rem'>Concrete, step-by-step illustrations of the paper's key techniques.</div>", unsafe_allow_html=True)

        examples = p.get("examples", [])
        if examples:
            for i, ex in enumerate(examples, 1):
                st.markdown(f"""
                <div style='display:flex;align-items:center;gap:10px;margin-bottom:.5rem'>
                    <span style='background:rgba(167,139,250,.12);border:1px solid rgba(167,139,250,.3);
                        color:#a78bfa;border-radius:50%;width:28px;height:28px;display:flex;
                        align-items:center;justify-content:center;font-size:.8rem;font-weight:700;
                        flex-shrink:0'>{i}</span>
                    <strong style='color:#e8eaf0'>{ex.get('title','')}</strong>
                </div>""", unsafe_allow_html=True)

                st.markdown(f"<div class='muted-text' style='margin-bottom:.75rem'>{ex.get('description','')}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='muted-text' style='white-space:pre-line;margin-bottom:.75rem'>{ex.get('content','')}</div>", unsafe_allow_html=True)

                if ex.get("code"):
                    st.markdown("<div class='section-label'>Pseudocode / Algorithm</div>", unsafe_allow_html=True)
                    st.code(ex["code"], language="python")

                if i < len(examples):
                    st.divider()
        else:
            st.info("No examples were generated for this paper.")

    # ────────────────────────────────────────────────────────────────────
    # TAB 5 — CHAT
    # ────────────────────────────────────────────────────────────────────
    with tabs[4]:
        st.markdown("## Ask Questions")
        st.markdown("<div class='muted-text' style='margin-bottom:1rem'>Ask anything about the paper — methodology, equations, results, comparisons, or intuitions.</div>", unsafe_allow_html=True)

        # Suggested questions
        sqs = p.get("suggested_questions", [])
        if sqs and not st.session_state.chat_history:
            st.markdown("**Suggested questions:**")
            cols = st.columns(min(len(sqs), 3))
            for idx, (col, sq) in enumerate(zip(cols * 2, sqs)):
                if idx < len(sqs):
                    with col:
                        if st.button(sq, key=f"sq_{idx}", use_container_width=True):
                            st.session_state.chat_history.append({"role": "user", "content": sq})
                            with st.spinner("Thinking..."):
                                answer = st.session_state.pipeline.answer_question(sq)
                            st.session_state.chat_history.append({"role": "assistant", "content": answer})
                            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Chat history display
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class='avatar-user'>You</div>
                <div class='chat-user'>{msg['content']}</div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("<div class='avatar-ai'>🔬 PaperLens AI</div>", unsafe_allow_html=True)
                with st.container():
                    st.markdown(msg["content"])
                    st.markdown("<br>", unsafe_allow_html=True)

        # Input box
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area(
                "Your question",
                placeholder="e.g. Can you explain the attention mechanism with a concrete example?",
                height=90,
                label_visibility="collapsed",
            )
            submitted = st.form_submit_button("Send →", type="primary", use_container_width=True)

        if submitted and user_input.strip():
            st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
            with st.spinner("Thinking..."):
                answer = st.session_state.pipeline.answer_question(user_input.strip())
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.rerun()

        if st.session_state.chat_history:
            if st.button("🗑 Clear chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
