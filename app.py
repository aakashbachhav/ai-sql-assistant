import streamlit as st
import pandas as pd
import ast

from langchain_community.utilities import SQLDatabase
from langchain_ollama import OllamaLLM
from langchain_experimental.sql import SQLDatabaseChain

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SQL Mind",
    page_icon="⬡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;500;600&family=Syne:wght@400;600;700;800&display=swap');

/* ── Reset & Root ── */
:root {
    --bg:        #0a0c0f;
    --surface:   #111318;
    --border:    #1e2230;
    --border-hi: #2e3450;
    --accent:    #00e5a0;
    --accent2:   #0084ff;
    --warn:      #ff6b35;
    --text:      #e2e8f0;
    --muted:     #5a6278;
    --mono:      'IBM Plex Mono', monospace;
    --sans:      'Syne', sans-serif;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

[data-testid="stAppViewContainer"] > .main {
    background-color: var(--bg) !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }
footer { display: none; }
#MainMenu { visibility: hidden; }

/* ── Typography ── */
h1, h2, h3, .stMarkdown h1, .stMarkdown h2 {
    font-family: var(--sans) !important;
}
p, li, div, span, label {
    font-family: var(--mono) !important;
}

/* ── Hero Header ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2rem;
    position: relative;
}

.hero-badge {
    display: inline-block;
    font-family: var(--mono);
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    border: 1px solid var(--accent);
    padding: 4px 14px;
    border-radius: 2px;
    margin-bottom: 1.2rem;
}

.hero-title {
    font-family: var(--sans) !important;
    font-size: 3.2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--text);
    line-height: 1;
    margin: 0 0 0.8rem;
}

.hero-title span {
    color: var(--accent);
}

.hero-sub {
    font-family: var(--mono);
    font-size: 0.8rem;
    color: var(--muted);
    letter-spacing: 0.05em;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-hi), transparent);
    margin: 0.5rem 0 2rem;
}

/* ── Input Area ── */
.stTextInput > div > div {
    background-color: var(--surface) !important;
    border: 1px solid var(--border-hi) !important;
    border-radius: 4px !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 0.85rem !important;
    transition: border-color 0.2s ease;
}

.stTextInput > div > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(0, 229, 160, 0.08) !important;
}

.stTextInput > div > div > input {
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 0.85rem !important;
    background: transparent !important;
}

.stTextInput > div > div > input::placeholder {
    color: var(--muted) !important;
}

.stTextInput label {
    font-family: var(--mono) !important;
    font-size: 0.7rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    margin-bottom: 6px !important;
}

/* ── Result Card ── */
.result-card {
    background: var(--surface);
    border: 1px solid var(--border-hi);
    border-radius: 4px;
    padding: 1.4rem 1.6rem;
    margin-top: 1.5rem;
    position: relative;
    overflow: hidden;
}

.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}

.result-label {
    font-family: var(--mono);
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 1rem;
}

.result-value {
    font-family: var(--mono);
    font-size: 1.05rem;
    font-weight: 500;
    color: var(--text);
    word-break: break-word;
}

/* ── Error / Info Banners ── */
.banner {
    border-radius: 4px;
    padding: 0.9rem 1.2rem;
    margin-top: 1rem;
    font-family: var(--mono);
    font-size: 0.78rem;
    line-height: 1.6;
}

.banner-error {
    background: rgba(255, 107, 53, 0.08);
    border: 1px solid rgba(255, 107, 53, 0.25);
    color: #ff9c72;
}

.banner-tip {
    background: rgba(0, 132, 255, 0.07);
    border: 1px solid rgba(0, 132, 255, 0.2);
    color: #5ab4ff;
    margin-top: 0.6rem;
}

/* ── Spinner override ── */
[data-testid="stSpinner"] div {
    font-family: var(--mono) !important;
    font-size: 0.8rem !important;
    color: var(--muted) !important;
}

/* ── Dataframe / Table ── */
[data-testid="stDataFrame"] {
    border-radius: 4px !important;
    overflow: hidden;
    border: 1px solid var(--border-hi) !important;
    margin-top: 0.5rem;
}

[data-testid="stDataFrame"] table {
    font-family: var(--mono) !important;
    font-size: 0.78rem !important;
}

[data-testid="stDataFrame"] thead tr th {
    background-color: #161923 !important;
    color: var(--accent) !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid var(--border-hi) !important;
}

[data-testid="stDataFrame"] tbody tr:hover td {
    background-color: rgba(0, 229, 160, 0.04) !important;
}

/* ── Suggestion Pills ── */
.pills-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 1.2rem;
}

.pill {
    display: inline-block;
    font-family: var(--mono);
    font-size: 0.7rem;
    color: var(--muted);
    border: 1px solid var(--border);
    border-radius: 2px;
    padding: 5px 12px;
    cursor: default;
    transition: all 0.15s;
}

.pill:hover {
    border-color: var(--accent);
    color: var(--accent);
}

/* ── Footer note ── */
.footnote {
    text-align: center;
    font-family: var(--mono);
    font-size: 0.62rem;
    color: var(--muted);
    margin-top: 3rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border);
    letter-spacing: 0.08em;
}
</style>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">⬡ Powered by CodeLlama</div>
    <h1 class="hero-title">SQL <span>Mind</span></h1>
    <p class="hero-sub">Query your sales database in plain English</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ── Backend Init (cached) ──────────────────────────────────────────────────────
@st.cache_resource
def init_chain():
    db = SQLDatabase.from_uri("sqlite:///sales.db")
    llm = OllamaLLM(
    model="codellama",
    temperature=0,
    base_url="http://host.docker.internal:11434"
)
    chain = SQLDatabaseChain.from_llm(llm=llm, db=db, verbose=False, return_direct=True)
    return chain

db_chain = init_chain()

# ── Input ──────────────────────────────────────────────────────────────────────
question = st.text_input(
    "YOUR QUESTION",
    placeholder="e.g.  Which country generated the highest sales?",
    label_visibility="visible",
)

# Suggestion pills (decorative)
st.markdown("""
<div class="pills-wrap">
    <span class="pill">Top products</span>
    <span class="pill">Monthly revenue</span>
    <span class="pill">Sales by region</span>
    <span class="pill">Best customers</span>
    <span class="pill">Order trends</span>
</div>
""", unsafe_allow_html=True)

# ── Query ──────────────────────────────────────────────────────────────────────
if question:
    with st.spinner("⬡  Translating to SQL and querying..."):
        try:
            response = db_chain.invoke({"query": question})

            if isinstance(response, dict) and "result" in response:
                result = response["result"]

                try:
                    data = ast.literal_eval(result)

                    if isinstance(data, list) and len(data) > 0:
                        # ── Table result ──────────────────────────────────────
                        df = pd.DataFrame(data)
                        num_cols = len(df.columns)

                        col_names = {
                            1: ["Result"],
                            2: ["Category", "Value"],
                            3: ["Column 1", "Column 2", "Column 3"],
                        }
                        df.columns = col_names.get(num_cols, [f"Col {i+1}" for i in range(num_cols)])

                        st.markdown("""
                        <div class="result-card">
                            <div class="result-label">Query Results</div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.dataframe(df, use_container_width=True, hide_index=True)
                        st.caption(f"↳ {len(df)} row{'s' if len(df) != 1 else ''} returned")

                    else:
                        # ── Single value result ───────────────────────────────
                        st.markdown(f"""
                        <div class="result-card">
                            <div class="result-label">Result</div>
                            <div class="result-value">{data}</div>
                        </div>
                        """, unsafe_allow_html=True)

                except (ValueError, SyntaxError):
                    # ── Plain text result ─────────────────────────────────────
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-label">Result</div>
                        <div class="result-value">{result}</div>
                    </div>
                    """, unsafe_allow_html=True)

            else:
                st.markdown(f"""
                <div class="result-card">
                    <div class="result-label">Result</div>
                    <div class="result-value">{response}</div>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.markdown(f"""
            <div class="banner banner-error">
                ✕ &nbsp; <strong>Error:</strong> {e}
            </div>
            <div class="banner banner-tip">
                ↳ Tip: Make sure your question refers to tables and columns that exist in the database.
            </div>
            """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footnote">
    SQL MIND · LOCAL LLM · NO DATA LEAVES YOUR MACHINE
</div>
""", unsafe_allow_html=True)