import streamlit as st
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Video Analyser",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ─── Import fonts ─────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ─── CSS tokens ────────────────────────────────────────────── */
:root {
  --bg:        #0a0d14;
  --surface:   #111520;
  --surface2:  #181d2e;
  --border:    #1f2640;
  --accent:    #6c63ff;
  --accent2:   #00d4aa;
  --accent3:   #ff6b6b;
  --text:      #e8eaf6;
  --muted:     #6b7280;
  --success:   #10b981;
  --warning:   #f59e0b;
}

/* ─── Base ──────────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.stApp {
    background: linear-gradient(135deg, #0a0d14 0%, #0d1020 50%, #0a0f1c 100%) !important;
    background-attachment: fixed !important;
}

/* ─── Hide Streamlit chrome ─────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2rem 4rem !important; max-width: 1200px !important; }

/* ─── Hero header ───────────────────────────────────────────── */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(90deg, rgba(108,99,255,0.15), rgba(0,212,170,0.15));
    border: 1px solid rgba(108,99,255,0.3);
    color: var(--accent2);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.35rem 1rem;
    border-radius: 999px;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-size: clamp(2.4rem, 5vw, 3.8rem);
    font-weight: 700;
    line-height: 1.1;
    margin: 0 0 1rem;
    background: linear-gradient(135deg, #ffffff 30%, var(--accent) 70%, var(--accent2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1.05rem;
    color: var(--muted);
    max-width: 560px;
    margin: 0 auto 0.6rem;
    line-height: 1.6;
    font-weight: 400;
}
.yt-notice {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(255,107,107,0.08);
    border: 1px solid rgba(255,107,107,0.2);
    border-radius: 8px;
    padding: 0.45rem 1rem;
    font-size: 0.8rem;
    color: #ff9999;
    margin-top: 0.6rem;
}

/* ─── Divider ───────────────────────────────────────────────── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 2rem 0;
}

/* ─── Cards ─────────────────────────────────────────────────── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.6rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}
.card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 16px;
    background: linear-gradient(135deg, rgba(108,99,255,0.04) 0%, transparent 60%);
    pointer-events: none;
}
.card-accent-purple::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), transparent);
    border-radius: 16px 16px 0 0;
}
.card-accent-teal::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent2), transparent);
    border-radius: 16px 16px 0 0;
}
.card-accent-red::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent3), transparent);
    border-radius: 16px 16px 0 0;
}

/* ─── Section headers ───────────────────────────────────────── */
.section-label {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.4rem;
}
.section-title {
    font-size: 1.15rem;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* ─── File uploader override ────────────────────────────────── */
[data-testid="stFileUploader"] {
    background: var(--surface2) !important;
    border: 2px dashed var(--border) !important;
    border-radius: 14px !important;
    padding: 1rem !important;
    transition: border-color 0.2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
}
[data-testid="stFileUploader"] label {
    color: var(--text) !important;
}

/* ─── Radio buttons ─────────────────────────────────────────── */
[data-testid="stRadio"] label {
    color: var(--text) !important;
    font-size: 0.92rem !important;
}
[data-testid="stRadio"] > div {
    gap: 1.2rem !important;
    flex-direction: row !important;
}

/* ─── Buttons ───────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent) 0%, #8b5cf6 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.8rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.02em !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s !important;
    box-shadow: 0 4px 20px rgba(108,99,255,0.3) !important;
}
.stButton > button:hover {
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ─── Text inputs ───────────────────────────────────────────── */
.stTextInput input, .stTextArea textarea {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.92rem !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(108,99,255,0.2) !important;
}

/* ─── Selectbox ─────────────────────────────────────────────── */
.stSelectbox > div > div {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}

/* ─── Expanders ─────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
[data-testid="stExpander"] summary {
    color: var(--text) !important;
    font-weight: 500 !important;
    padding: 0.8rem 1rem !important;
}

/* ─── Metrics ───────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
}
[data-testid="stMetricValue"] {
    color: var(--accent) !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
}
[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}

/* ─── Chat bubble ───────────────────────────────────────────── */
.chat-msg {
    display: flex;
    gap: 0.8rem;
    margin-bottom: 1rem;
    align-items: flex-start;
}
.chat-avatar {
    width: 34px; height: 34px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}
.avatar-user   { background: linear-gradient(135deg, var(--accent), #8b5cf6); }
.avatar-bot    { background: linear-gradient(135deg, var(--accent2), #0891b2); }
.chat-bubble {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
    line-height: 1.55;
    max-width: 85%;
    color: var(--text);
}
.chat-bubble-user {
    background: rgba(108,99,255,0.12);
    border-color: rgba(108,99,255,0.25);
}

/* ─── Progress override ─────────────────────────────────────── */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
    border-radius: 999px !important;
}

/* ─── Alert / info boxes ────────────────────────────────────── */
.stAlert {
    background: var(--surface2) !important;
    border-radius: 10px !important;
}

/* ─── Mono transcript ───────────────────────────────────────── */
.transcript-box {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
    line-height: 1.7;
    color: #a8b4d0;
    max-height: 280px;
    overflow-y: auto;
    white-space: pre-wrap;
}
.transcript-box::-webkit-scrollbar { width: 6px; }
.transcript-box::-webkit-scrollbar-track { background: transparent; }
.transcript-box::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* ─── Tag pills ─────────────────────────────────────────────── */
.tag {
    display: inline-block;
    background: rgba(108,99,255,0.12);
    border: 1px solid rgba(108,99,255,0.25);
    color: #a89bff;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    padding: 0.2rem 0.65rem;
    border-radius: 999px;
    margin-right: 0.4rem;
}
.tag-teal {
    background: rgba(0,212,170,0.1);
    border-color: rgba(0,212,170,0.25);
    color: #6ee8d0;
}
.tag-red {
    background: rgba(255,107,107,0.1);
    border-color: rgba(255,107,107,0.2);
    color: #ffaaaa;
}

/* ─── Spinner text ──────────────────────────────────────────── */
[data-testid="stSpinner"] p {
    color: var(--muted) !important;
    font-size: 0.88rem !important;
}
</style>
""", unsafe_allow_html=True)


# ── Session state init ──────────────────────────────────────────────────────────
for key in ["results", "rag_chain", "chat_history", "processing"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "chat_history" else []


# ══════════════════════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ Powered by Whisper · Mistral · ChromaDB</div>
    <h1 class="hero-title">AI Video Analyser</h1>
    <p class="hero-sub">
        Upload any audio or video file and instantly extract a transcript,
        smart summary, action items, key decisions, and open questions —
        then chat with your content.
    </p>
    <div class="yt-notice">
        ⚠️ YouTube has denied access for their videos — please upload a local file instead.
    </div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
#  UPLOAD + SETTINGS
# ══════════════════════════════════════════════════════════════════════
col_upload, col_settings = st.columns([3, 2], gap="large")

with col_upload:
    st.markdown("""
    <div class="card card-accent-purple">
        <div class="section-label">Step 1</div>
        <div class="section-title">🎬 Upload Your File</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        label="Drop your media file here",
        type=["mp3", "mp4", "wav", "m4a"],
        help="Supported formats: MP3, MP4, WAV, M4A",
        label_visibility="collapsed",
    )

    if uploaded_file:
        # Show file info pills
        size_mb = uploaded_file.size / (1024 * 1024)
        ext = uploaded_file.name.split(".")[-1].upper()
        st.markdown(f"""
        <div style="margin-top:0.8rem; display:flex; align-items:center; gap:0.6rem; flex-wrap:wrap;">
            <span class="tag">📄 {uploaded_file.name}</span>
            <span class="tag-teal">{ext}</span>
            <span class="tag">{size_mb:.1f} MB</span>
        </div>
        """, unsafe_allow_html=True)

with col_settings:
    st.markdown("""
    <div class="card card-accent-teal">
        <div class="section-label">Step 2</div>
        <div class="section-title">⚙️ Settings</div>
    </div>
    """, unsafe_allow_html=True)

    language = st.radio(
        "Audio Language",
        options=["english", "hinglish"],
        format_func=lambda x: "🇬🇧 English" if x == "english" else "🇮🇳 Hinglish",
        horizontal=True,
        help=(
            "English → local Whisper model\n"
            "Hinglish → Sarvam STT (translates to English)"
        ),
    )

    st.markdown("""
    <div style="margin-top:1rem; background:rgba(108,99,255,0.06); border:1px solid rgba(108,99,255,0.15);
                border-radius:10px; padding:0.8rem 1rem; font-size:0.82rem; color:#8890a6; line-height:1.5;">
        <b style="color:#a89bff;">English</b> uses the local <code>Whisper</code> model.<br>
        <b style="color:#6ee8d0;">Hinglish</b> uses <code>Sarvam STT</code> and auto-translates to English.
    </div>
    """, unsafe_allow_html=True)


# ── Analyse button ──────────────────────────────────────────────────────────────
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

run_col, _ = st.columns([1, 3])
with run_col:
    analyse_clicked = st.button("🚀 Analyse", use_container_width=True, disabled=(uploaded_file is None))

if uploaded_file and analyse_clicked:
    # Save uploaded file to a temp path so our pipeline can read it
    suffix = "." + uploaded_file.name.rsplit(".", 1)[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    progress_bar = st.progress(0, text="Initialising pipeline…")

    try:
        from utils.audio_processor import process_input
        from core.transcriber import transcribe_all
        from core.summarizer import summarize, generate_title
        from core.extractor import extract_action_items, extract_key_decisions, extract_questions
        from core.rag_engine import build_rag_chain

        progress_bar.progress(5, text="🔊 Processing audio…")
        chunks = process_input(tmp_path)

        progress_bar.progress(25, text="📝 Transcribing audio…")
        transcript = transcribe_all(chunks, language)

        progress_bar.progress(50, text="✍️ Generating title & summary…")
        title   = generate_title(transcript)
        summary = summarize(transcript)

        progress_bar.progress(65, text="✅ Extracting action items…")
        action_items = extract_action_items(transcript)

        progress_bar.progress(75, text="🔑 Extracting key decisions…")
        decisions = extract_key_decisions(transcript)

        progress_bar.progress(85, text="❓ Extracting open questions…")
        questions = extract_questions(transcript)

        progress_bar.progress(95, text="🧠 Building RAG chain…")
        rag_chain = build_rag_chain(transcript)

        progress_bar.progress(100, text="✅ Done!")

        st.session_state.results = {
            "title":        title,
            "transcript":   transcript,
            "summary":      summary,
            "action_items": action_items,
            "key_decisions": decisions,
            "open_questions": questions,
        }
        st.session_state.rag_chain    = rag_chain
        st.session_state.chat_history = []

    except Exception as e:
        progress_bar.empty()
        st.error(f"❌ Pipeline error: {e}")
    finally:
        os.unlink(tmp_path)


# ══════════════════════════════════════════════════════════════════════
#  RESULTS
# ══════════════════════════════════════════════════════════════════════
if st.session_state.results:
    res = st.session_state.results

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ── Title banner ──────────────────────────────────────────────────
    st.markdown(f"""
    <div class="card" style="text-align:center; padding:2rem 1.6rem;">
        <div class="section-label">Meeting / Video Title</div>
        <h2 style="font-size:1.7rem; font-weight:700; margin:0.4rem 0 0;
                   background:linear-gradient(135deg,#fff 30%,#6c63ff 70%,#00d4aa 100%);
                   -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;">
            📌 {res['title']}
        </h2>
    </div>
    """, unsafe_allow_html=True)

    # ── Transcript (collapsed) ────────────────────────────────────────
    with st.expander("📜 Full Transcript", expanded=False):
        st.markdown(f'<div class="transcript-box">{res["transcript"]}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

    # ── 3-column insights ─────────────────────────────────────────────
    col_a, col_b, col_c = st.columns(3, gap="medium")

    with col_a:
        st.markdown("""
        <div class="card card-accent-purple">
            <div class="section-label">Output</div>
            <div class="section-title">📋 Summary</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(res["summary"])

    with col_b:
        st.markdown("""
        <div class="card card-accent-teal">
            <div class="section-label">Output</div>
            <div class="section-title">✅ Action Items</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(res["action_items"])

    with col_c:
        st.markdown("""
        <div class="card card-accent-red">
            <div class="section-label">Output</div>
            <div class="section-title">🔑 Key Decisions</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(res["key_decisions"])

    st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)

    # ── Open questions ────────────────────────────────────────────────
    st.markdown("""
    <div class="card">
        <div class="section-label">Output</div>
        <div class="section-title">❓ Open Questions & Follow-ups</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(res["open_questions"])


# ══════════════════════════════════════════════════════════════════════
#  RAG CHAT
# ══════════════════════════════════════════════════════════════════════
if st.session_state.rag_chain is not None:

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card card-accent-purple">
        <div class="section-label">Phase 2</div>
        <div class="section-title">💬 Chat with Your Content</div>
        <p style="color:#6b7280; font-size:0.88rem; margin:0; line-height:1.5;">
            Ask anything about the video or meeting. The assistant answers only
            from what's in the transcript — no hallucinations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── Render chat history ───────────────────────────────────────────
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="chat-msg" style="justify-content:flex-end;">
                <div class="chat-bubble chat-bubble-user">{msg["content"]}</div>
                <div class="chat-avatar avatar-user">👤</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-msg">
                <div class="chat-avatar avatar-bot">🤖</div>
                <div class="chat-bubble">{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Input row ─────────────────────────────────────────────────────
    q_col, btn_col = st.columns([5, 1], gap="small")
    with q_col:
        question = st.text_input(
            label="question",
            placeholder="Ask something about the transcript…",
            label_visibility="collapsed",
            key="chat_input",
        )
    with btn_col:
        send = st.button("Send ➤", use_container_width=True)

    if send and question.strip():
        from core.rag_engine import ask_question

        st.session_state.chat_history.append({"role": "user", "content": question.strip()})

        with st.spinner("Thinking…"):
            answer = ask_question(st.session_state.rag_chain, question.strip())

        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

    # ── Clear chat ────────────────────────────────────────────────────
    if st.session_state.chat_history:
        if st.button("🗑 Clear chat", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()


# ══════════════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════════════
st.markdown("<div class='divider' style='margin-top:3rem;'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; padding-bottom:2rem;">
    <p style="color:#374151; font-size:0.78rem; font-family:'Space Grotesk',sans-serif; margin:0;">
        AI Video Analyser &nbsp;·&nbsp; Whisper &nbsp;·&nbsp; Mistral &nbsp;·&nbsp; ChromaDB &nbsp;·&nbsp; Sarvam STT
    </p>
</div>
""", unsafe_allow_html=True)
