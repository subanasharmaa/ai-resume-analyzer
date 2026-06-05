import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import pymupdf , io

load_dotenv()

st.set_page_config(page_title="Resume Scorer", layout="centered")

st.markdown("""
<style>
    .stApp { background: #f0f6ff; }
    .header { background: #1a56db; padding: 1.5rem; border-radius: 12px; text-align: center; margin-bottom: 1.5rem; }
    .header h2 { color: white; margin: 0; }
    .header p  { color: #bfdbfe; margin: 0.3rem 0 0; font-size: 0.9rem; }
    .stButton > button { background: #1a56db; color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%; }
    .stButton > button:hover { background: #1648c0; }
    .win { background: white; border-left: 4px solid #1a56db; border-radius: 8px; padding: 0.7rem 1rem; margin-bottom: 0.5rem; }
</style>
<div class="header">
    <h2>Resume Scorer</h2>
    <p>Score your resume across 6 categories</p>
</div>
""", unsafe_allow_html=True)

def parse_pdf(file_bytes):
    doc = pymupdf.open(stream=io.BytesIO(file_bytes), filetype="pdf")
    return "\n\n".join(page.get_text() for page in doc)

uploaded = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

if uploaded is not None:
    file_bytes = uploaded.getvalue()
    if file_bytes and st.session_state.get("resume_name") != uploaded.name:
        st.session_state["resume_text"] = parse_pdf(file_bytes)
        st.session_state["resume_name"] = uploaded.name

resume = st.session_state.get("resume_text")

if resume:
    st.success("Resume ready: " + st.session_state["resume_name"])

job_role = st.text_input("Target Job Role (optional)", placeholder="e.g. Data Analyst")

if st.button("Score My Resume"):
    if not resume:
        st.warning("Please upload your resume first.")
    else:
        prompt = PromptTemplate(
            input_variables=["resume", "job_role"],
            template="""
You are a resume scoring expert.
Score the resume across 6 categories out of 10.
Target job role: {job_role}

Resume:
{resume}

Reply in EXACTLY this format with no extra text:

CLARITY: X/10 - reason
FORMAT: X/10 - reason
SKILLS: X/10 - reason
EXPERIENCE: X/10 - reason
IMPACT: X/10 - reason
ATS: X/10 - reason

OVERALL: XX/100

TOP 3 QUICK WINS:
1. ...
2. ...
3. ...
"""
        )
        llm = ChatOpenAI(model="gpt-4o")
        chain = prompt | llm | StrOutputParser()

        with st.spinner("Scoring your resume..."):
            result = chain.invoke({
                "resume": resume,
                "job_role": job_role.strip() or "Not specified"
            })

        categories = ["CLARITY", "FORMAT", "SKILLS", "EXPERIENCE", "IMPACT", "ATS"]
        scores, reasons = {}, {}

        for line in result.split("\n"):
            for cat in categories:
                if line.startswith(cat + ":"):
                    try:
                        parts = line.split("-")
                        scores[cat] = int(parts[0].split(":")[1].strip().split("/")[0])
                        reasons[cat] = parts[1].strip() if len(parts) > 1 else ""
                    except:
                        pass

        overall = None
        for line in result.split("\n"):
            if line.startswith("OVERALL:"):
                try:
                    overall = int(line.split(":")[1].strip().split("/")[0])
                except:
                    pass

        st.markdown("---")

        if overall:
            color = "#16a34a" if overall >= 75 else "#d97706" if overall >= 50 else "#dc2626"
            st.markdown(f"""
            <div style="background:{color};color:white;text-align:center;
                        border-radius:12px;padding:1rem;margin-bottom:1.2rem;">
                <div style="font-size:0.85rem;">Overall Score</div>
                <div style="font-size:2.8rem;font-weight:700;">{overall}/100</div>
            </div>""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        for i, cat in enumerate(categories):
            score = scores.get(cat, 0)
            bar_color = "#1a56db" if score >= 7 else "#d97706" if score >= 5 else "#dc2626"
            with (col1 if i % 2 == 0 else col2):
                st.markdown(f"""
                <div style="background:white;border-radius:10px;padding:0.9rem;
                            margin-bottom:0.7rem;border:1px solid #e5e7eb;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:5px;">
                        <span style="font-weight:600;color:#1a56db;">{cat}</span>
                        <span style="font-weight:700;color:{bar_color};">{score}/10</span>
                    </div>
                    <div style="background:#e5e7eb;border-radius:50px;height:7px;">
                        <div style="background:{bar_color};width:{score*10}%;height:7px;border-radius:50px;"></div>
                    </div>
                    <div style="font-size:0.78rem;color:#6b7280;margin-top:5px;">
                        {reasons.get(cat, "")}
                    </div>
                </div>""", unsafe_allow_html=True)

        st.markdown("#### Top 3 Quick Wins")
        in_wins = False
        for line in result.split("\n"):
            if "TOP 3 QUICK WINS" in line:
                in_wins = True
                continue
            if in_wins and line.strip().startswith(("1.", "2.", "3.")):
                st.markdown(f'<div class="win">{line.strip()}</div>', unsafe_allow_html=True)