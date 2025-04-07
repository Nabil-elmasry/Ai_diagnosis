
import streamlit as st
import pdfplumber
import pandas as pd

st.set_page_config(page_title="AI Diagnosis", layout="wide")
st.title("Vehicle Fault Diagnosis (AI Assistant)")

def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

st.sidebar.header("Upload Diagnosis Files")
sensor_pdf = st.sidebar.file_uploader("Upload Sensor Data (PDF)", type="pdf")
code_pdf = st.sidebar.file_uploader("Upload Fault Report (PDF)", type="pdf")

if sensor_pdf and code_pdf:
    st.subheader("1. Sensor Data Content")
    sensor_text = extract_text_from_pdf(sensor_pdf)
    st.text_area("Sensor Data", sensor_text, height=300)

    st.subheader("2. Fault Code Report")
    code_text = extract_text_from_pdf(code_pdf)
    st.text_area("Fault Report", code_text, height=300)

    st.subheader("3. AI Initial Insight")
    st.markdown("- Based on your sensor and fault code data, further analysis will be applied here.")
    st.info("**Next Step:** This area will display fault reason detection + recommended solutions.")
else:
    st.warning("Please upload both PDF files to start the diagnosis.")