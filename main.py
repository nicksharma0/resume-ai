import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI

st.set_page_config(page_title="Cold Email Generator", page_icon="📨", layout="centered")

st.title("AI Cold Email Generator 📩")
st.markdown("Upload your resume and specify the type of position you're seeking. Our AI-powered tool will instantly generate a **professional** cold email tailored to help you **stand out** to recruiters and hiring managers.")
st.markdown("---")
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

uploaded_file = st.file_uploader("Upload your resume as a PDF or txt.", type=["pdf", "txt"])
job_role = st.text_input("Enter the job/role you are targetting (Optional)")

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
        I want to write a compelling cold email to a hiring manager or recruiter. I'll provide the content of my resume, and optionally the type of job I'm targeting. Based on this, can you generate a short, professional cold email that introduces me, highlights key qualifications, and expresses interest in relevant opportunities?

        Here is my resume:
        {file_content}

        The job I am looking for is:
        {job_role if job_role else 'a position that aligns with my background'}

        Please make sure the tone is professional but approachable, and keep the email concise (around 150–200 words).
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
