import streamlit as st
if "resume_text" not in st.session_state:
    st.session_state["resume_text"] = None
if "resume_name" not in st.session_state:
    st.session_state["resume_name"] = None

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

st.markdown("""
<style>
    .stApp { background: #f0f6ff; }
    .header { background: #1a56db; padding: 2rem; border-radius: 12px; text-align: center; margin-bottom: 2rem; }
    .header h1 { color: white; margin: 0; font-size: 2rem; }
    .header p  { color: #bfdbfe; margin: 0.4rem 0 0; }
    .card { background: white; border: 1px solid #e5e7eb; border-radius: 10px; padding: 1.2rem 1.5rem; margin-bottom: 1rem; }
    .card h4 { color: #1a56db; margin: 0 0 0.3rem; }
    .card p  { color: #6b7280; margin: 0; font-size: 0.9rem; }
</style>
<div class="header">
    <h1>AI Resume Analyzer</h1>
    <p>Pick a tool from the sidebar to get started</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="card"><h4>Resume Checker</h4><p>Full AI evaluation with score, strengths and weaknesses.</p></div>', unsafe_allow_html=True)
st.markdown('<div class="card"><h4>Resume Scorer</h4><p>Score across 6 categories with quick win tips.</p></div>', unsafe_allow_html=True)
st.markdown('<div class="card"><h4>Cover Letter Generator</h4><p>Tailored cover letter for any job.</p></div>', unsafe_allow_html=True)
st.markdown('<div class="card"><h4>AI Career Coach</h4><p>Chat with an AI career coach for personalized advice.</p></div>', unsafe_allow_html=True)