import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Resume Critiquer", page_icon="📄", layout="centered")

st.title("AI Resume Review")
st.markdown("Upload your resume and get AI powered feedback tailored to your needs.")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

uploaded_file = st.file_uploader("Upload your resume as a PDF or txt.", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role you are targetting (Optional)")

analyze = st.button("Analyze Resume")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

if analyze:
    try:
        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("File does not have readable content.")
            st.stop()

        prompt = f"""
        I'm looking for help improving my resume. I'll share the content of my current resume along with the job description for the position I'm applying to. Can you give me constructive feedback on how to make my resume more compelling for this specific role? Please focus on clarity, relevance, formatting, keyword alignment with the job description, and any ways I can better highlight my achievements and skills.

        Here is my resume:
        {file_content}

        The job I am looking for is:
        {job_role if job_role else 'general job applications'}

        """
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert resume reviewer with years of experience in HR and recruitment."},
                {"role": "user", "content": prompt}
            ],
            temperature= .7,
            max_tokens = 1000
        )
        st.markdown('### Analysis Results')
        st.markdown(response.choices[0].message.content)
    
    except Exception as e:
        st.error(f"An error occured: {(str(e))}")
