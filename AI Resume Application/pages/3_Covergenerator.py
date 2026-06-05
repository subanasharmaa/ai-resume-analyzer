import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import pymupdf , io
load_dotenv()

st.set_page_config(page_title="Cover Letter Generator", layout="centered")

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
    <h2>Cover Letter Generator</h2>
    <p>Generate a tailored cover letter from your resume</p>
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

col1, col2 = st.columns(2)
with col1:
    job_title = st.text_input("Job Title", placeholder="e.g. Data Scientist")
with col2:
    company = st.text_input("Company Name", placeholder="e.g. Google")

job_description = st.text_area("Job Description", placeholder="Paste the job description here...", height=150)

if st.button("Generate Cover Letter"):
    if not resume:
        st.warning("Please upload your resume first.")
    elif not job_title.strip():
        st.warning("Please enter the job title.")
    elif not company.strip():
        st.warning("Please enter the company name.")
    elif not job_description.strip():
        st.warning("Please enter the job description.")
    else:
        prompt = PromptTemplate(
            input_variables=["resume", "job_title", "company", "job_description"],
            template="""
You are a professional cover letter writer.
Write a cover letter using the resume below.

Resume:
{resume}

Job Title: {job_title}
Company: {company}
Job Description: {job_description}

The cover letter must have:
1. A strong opening showing enthusiasm for the role
2. A middle paragraph connecting resume skills to the job
3. A closing paragraph with a call to action

Keep the tone confident and human. Do not use placeholders like [Your Name] or [Date].
Write it as a complete ready-to-send letter.
"""
        )
        llm = ChatOpenAI(model="gpt-4o")
        chain = prompt | llm | StrOutputParser()

        with st.spinner("Writing your cover letter..."):
            result = chain.invoke({
                "resume": resume,
                "job_title": job_title.strip(),
                "company": company.strip(),
                "job_description": job_description.strip()
            })

        st.markdown('<div class="result">', unsafe_allow_html=True)
        st.markdown(result)
        st.markdown('</div>', unsafe_allow_html=True)

        st.download_button(
            "Download Cover Letter",
            data=result,
            file_name=f"cover_letter_{company.strip().replace(' ', '_')}.txt"
        )