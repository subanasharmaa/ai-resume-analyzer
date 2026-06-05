import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import pymupdf , io

load_dotenv()

st.set_page_config(page_title="AI Career Coach", layout="centered")

st.markdown("""
<style>
    .stApp { background: #f0f6ff; }
    .header { background: #1a56db; padding: 1.5rem; border-radius: 12px; text-align: center; margin-bottom: 1.5rem; }
    .header h2 { color: white; margin: 0; }
    .header p  { color: #bfdbfe; margin: 0.3rem 0 0; font-size: 0.9rem; }
    .stButton > button { background: #1a56db; color: white; border: none; border-radius: 8px; font-weight: 600; width: 100%; }
    .stButton > button:hover { background: #1648c0; }
</style>
<div class="header">
    <h2>AI Career Coach</h2>
    <p>Chat with an AI coach that knows your resume</p>
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

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if resume and len(st.session_state["chat_history"]) == 0:
    st.markdown("**Try asking:**")
    col1, col2 = st.columns(2)
    suggestions = [
        "What are my strongest skills?",
        "What jobs should I apply for?",
        "How can I improve my resume?",
        "What salary should I expect?",
    ]
    for i, suggestion in enumerate(suggestions):
        with (col1 if i % 2 == 0 else col2):
            if st.button(suggestion, key=f"s{i}"):
                st.session_state["quick_q"] = suggestion

for msg in st.session_state["chat_history"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask your career coach...", disabled=not resume)

if "quick_q" in st.session_state:
    user_input = st.session_state.pop("quick_q")

if user_input:
    if not resume:
        st.warning("Please upload your resume first.")
    else:
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state["chat_history"].append({"role": "user", "content": user_input})

        history_text = ""
        for msg in st.session_state["chat_history"][:-1]:
            role = "Candidate" if msg["role"] == "user" else "Coach"
            history_text += f"{role}: {msg['content']}\n"

        prompt = PromptTemplate(
            input_variables=["resume", "history", "question"],
            template="""
You are an experienced career coach who has read the candidate's resume.
Give practical and specific advice based on their background.
Keep your answer to 3 to 5 sentences unless more detail is needed.

Resume:
{resume}

Conversation so far:
{history}

Candidate question: {question}

Your response:
"""
        )
        llm = ChatOpenAI(model="gpt-4o")
        chain = prompt | llm | StrOutputParser()

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = chain.invoke({
                    "resume": resume,
                    "history": history_text or "No previous conversation.",
                    "question": user_input
                })
            st.markdown(reply)

        st.session_state["chat_history"].append({"role": "assistant", "content": reply})

if st.session_state["chat_history"]:
    st.markdown("---")
    if st.button("Clear Chat"):
        st.session_state["chat_history"] = []
        st.rerun()