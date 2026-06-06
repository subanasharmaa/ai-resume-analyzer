# ai-resume-analyzer
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/LangChain-🦜-121212?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/OpenAI-GPT--4o-412991?style=for-the-badge&logo=openai&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/PyMuPDF-306998?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge"/>
</p>
<p align="center">
  <strong>A simple but powerful web app that reads your resume and tells you exactly how to improve it.</strong><br/>
  Upload your PDF, get an AI evaluation, score breakdown, tailored cover letter, and chat with a career coach that actually knows your background.
</p>

<details>
<summary>📋 Table of Contents</summary>

- [About the Project](#-about-the-project)
- [Features](#-features)
- [Limitations](#-Limitations)
- [How It Works](#-how-it-works)
- [App Flow Architecture](#-app-flow-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
- [Usage](#-usage)
- [Screenshots](#-screenshots)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

</details>

**About the Project**
ai-resume-analyzer is a multi-page Streamlit application built for students and job seekers who want real, specific feedback on their resume.
Getting honest, specific feedback on a resume is harder than it should be. Most tools give you a checklist. Most people give you vague advice. Neither tells you what is actually wrong with actual resume.

**ai-resume-analyzer** solves that by reading your resume directly and responding based on your real content. Every evaluation, every score, every cover letter generated from what you have actually written, not a generic template.

The project is built around four tools that cover the most common resume-related tasks a job seeker needs. The kind of tool that would have saved a lot of time during internship application season.

Under the hood it uses LangChain LCEL chains to pipe resume text through structured prompts to GPT-4o, with Streamlit handling the multi-page UI and session state. The architecture is intentionally simple — no vector databases, no embeddings. Just clean prompt design and a reliable PDF parser doing the heavy lifting.


**How It Works**

User uploads a PDF resume on any page.
PyMuPDF extracts the raw text from the PDF.
Extracted text is stored in Streamlit session state and persists across reruns.
Text is injected into a LangChain PromptTemplate along with any user inputs.
The prompt is piped through the LangChain LCEL chain to GPT-4o.
The response is parsed and displayed with structured UI components.
For the AI Coach, full conversation history is passed on every turn for multi-turn memory.

**Features**

📊 Resume Checker — full AI evaluation with overall score out of 100, strengths, weaknesses, skills found, missing skills, and suggested career steps.


🏆 Resume Scorer — scores your resume across 6 categories (Clarity, Format, Skills, Experience, Impact, ATS) with visual progress bars and top 3 quick wins.


✉️ Cover Letter Generator — generates a complete, ready-to-send cover letter tailored to a specific job title, company, and job description.


🤖 AI Career Coach — a multi-turn chat interface where the AI has read your resume and gives specific, practical advice based on your real background.

📥 Download reports — save your analysis or cover letter as a .txt file.


🔒 Persistent upload — resume stays loaded across button clicks and reruns without re-uploading.


🎨 Clean minimal UI — blue and white Streamlit interface, no clutter.

## Known Limitations

I'll be honest — this project works great for most resumes, but it is not perfect. Here is what I ran into while building and testing it.

**Designed and template-based resumes** — resumes made in Canva, Novoresume, or any heavily styled resume builder sometimes parse badly. The text comes out incomplete or can't process because PyMuPDF reads the raw PDF structure, and fancy layouts do not always store text the way you would expect. If your resume looks beautiful but the app gives weird results, this is probably why.

**Scanned or image resumes** — if your resume is a photo or a scanned document inside a PDF, the app will not be able to read it at all. PyMuPDF extracts text, not images. Adding proper OCR support is on the roadmap but is not built yet.

**No multi-column layout support** — resumes with two-column layouts may have their text extracted in the wrong reading order, which can confuse the AI evaluation.

**What works best** — a clean, single-column PDF resume exported directly from a word processor or a simple resume builder. If you are unsure, open your PDF in a browser, try to select and copy the text — if you can copy it, the app can read it.

I am aware of these gaps and they are on the roadmap. I built this during my internship preparation to get hands-on with LangChain and Streamlit, and it served that purpose well- but there is definitely room to grow.


**Architecture Flow Diagram**
<img width="1102" height="1006" alt="image" src="https://github.com/user-attachments/assets/32147f01-eef6-4fd8-a018-9a558c4a1015" />

**Tech Stack**
| Layer | Technology |
|-------|------------|
| **LLM** | OpenAI GPT-4o |
| **LLM Framework** | LangChain LCEL |
| **Frontend** | Streamlit |
| **PDF Parsing** | PyMuPDF (fitz) |
| **Environment** | Python-dotenv |

# Project Structure
```text
ai-resume-analyzer/
│
├── main.py                       # Home page — sidebar navigation
│
├── pages/
│   ├── 1_Resumechecker.py        # Full resume evaluation page
│   ├── 2_Resumescorer.py         # Category-wise scoring with progress bars
│   ├── 3_Covergenerator.py       # Cover letter generation page
│   └── 4_Aicoach.py              # Multi-turn AI career coach chat
│
├── .env                          # API keys 
├── .gitignore                    # Excludes .env, .venv, __pycache__
├── requirements.txt              # All Python dependencies
└── README.md
``` 
**Getting Started**
Prerequisites
Python 3.10 or higher
An OpenAI API key

**Installation**
1. Clone the repository
   - git clone https://github.com/your-username/ai-resume-analyzer.git
cd ai-resume-analyzer
2.Create and activate a virtual environment
   python -m venv venv
    **On macOS/Linux**
   source venv/bin/activate
    **On Windows**
   venv\Scripts\activate
3. Install dependencies
   pip install -r requirements.txt
   
**Environment Variables**
Create a .env file in the project root:
OPENAI_API_KEY=your_openai_api_key_here
**Usages**
Run the Streamlit app:
--streamlit run app.py
Then open your browser at http://localhost:8501
--Pick any tool from the sidebar
--Upload your resume PDF on that page
--Fill in any required inputs and click the action button
--Download your result if needed

**Screenshots**
|       Page              Screenshot    |


| **Home**   <img width="1713" height="850" alt="image" src="https://github.com/user-attachments/assets/fdb57526-  46fb-4573-82f2-da1516233f15" />


             <img width="1108" height="458" alt="image" src="https://github.com/user-attachments/assets/64fd5325- 1a1e-4299-8e91-b7f8b9dfa474" />


| **Resumechecker**  <img width="1740" height="570" alt="image" src="https://github.com/user-          attachments/assets/1e8e133e-f3c6-4164-989a-0c08d4ad652e" />
 

| **Resumescorer**      <img width="1733" height="702" alt="image" src="https://github.com/user-attachments/assets/3fcbc00e-6f0e-429b-86fd-4135c18ed461" />
    

| **Coverlettergenerator** <img width="1735" height="840" alt="image" src="https://github.com/user-attachments/assets/c4d064bf-b56f-4da5-a4d4-c109327621f6" />


 **AIcoach**            <img width="1732" height="782" alt="image" src="https://github.com/user-attachments/assets/885a8467-b637-422e-9ae7-a7e238828487" />



**Roadmap**

 -Add support for DOCX resume uploads
 -Add job description matching score
 -LinkedIn profile analyzer
 -Interview question generator based on resume
 -Deploy to Streamlit Cloud
 -Support multiple resume versions for comparison
 -Add resume rewriting suggestions inline
 -Export full analysis as a PDF report

 **Contributing**
Contributions are welcome. Here is how to get started:
Fork the repository
Create a new branch (git checkout -b feature/your-feature-name)
Commit your changes (git commit -m 'Add some feature')
Push to the branch (git push origin feature/your-feature-name)
Open a Pull Request

**License**
This project is licensed under the MIT License — see the LICENSE file for details.

<p align="center">
  Built with curiosity and a lot of debugging — by a 6th sem CS student
</p>

