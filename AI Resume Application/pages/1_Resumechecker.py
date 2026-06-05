import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import pymupdf , io
load_dotenv()

st.set_page_config(page_title="Resume Checker", layout="centered")

st.markdown("""
<style>
    .stApp { background: #f0f6ff; }
    .header { background: #1a56db; padding: 1.5rem; border-radius: 12px; text-align: center; margin-bottom: 1.5rem; }
    .header h2 { color: white; margin: 0; }
    .header p  { color: #bfdbfe; margin: 0.3rem 0 0; font-size: 0.9rem; }
    .stButton > button { background: #1a56db; color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%; }
    .stButton > button:hover { background: #1648c0; }
    .result { background: white; border-left: 4px solid #1a56db; border-radius: 10px; padding: 1.2rem 1.5rem; margin-top: 1rem; }
</style>
<div class="header">
    <h2>Resume Checker</h2>
    <p>Get an AI evaluation of your resume</p>
</div>
""", unsafe_allow_html=True)

def parse_pdf(file_bytes):
    doc = pymupdf.open(stream=io.BytesIO(file_bytes), filetype="pdf")
    return "\n\n".join(page.get_text() for page in doc)

uploaded = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

if uploaded is not None:
    file_bytes = uploaded.getvalue()
    if file_bytes and st.session_state.get("resume_name") != uploaded.name:
        text = parse_pdf(file_bytes)
        st.session_state["resume_text"] = text
        st.session_state["resume_name"] = uploaded.name
resume = st.session_state.get("resume_text")

if resume and resume.strip():
    st.success("Resume ready: " + st.session_state["resume_name"])
if st.button("Analyse Resume"):
    if not resume or not resume.strip():
        st.warning("Please upload your resume first.")
    else:
        prompt = PromptTemplate(
            input_variables=["resume"],
            template="""
You are a professional resume evaluator.

Analyse the resume below and provide:
1. Overall Score out of 100
2. Strengths (minimum 3 points)
3. Weaknesses (minimum 3 points)
4. Skills found in the resume
5. Skills missing that would improve it
6. Recommended next career steps

Resume:
{resume}
"""
        )
        llm = ChatOpenAI(model="gpt-4o")
        chain = prompt | llm | StrOutputParser()

        with st.spinner("Analysing your resume..."):
            result = chain.invoke({"resume": resume})

        st.markdown('<div class="result">', unsafe_allow_html=True)
        st.markdown(result)
        st.markdown('</div>', unsafe_allow_html=True)

        st.download_button("Download Report", data=result, file_name="resume_report.txt")