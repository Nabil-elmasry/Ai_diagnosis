
import streamlit as st
import pandas as pd
import pdfplumber
import io

st.set_page_config(page_title="AI Diagnosis", layout="wide")

st.title("AI Car Diagnostic Tool")

st.markdown("Upload **Fault Report** and **Sensor Report** as PDF files")

col1, col2 = st.columns(2)

with col1:
    fault_pdf = st.file_uploader("Upload Fault Report PDF", type="pdf", key="fault")
with col2:
    sensor_pdf = st.file_uploader("Upload Sensor Report PDF", type="pdf", key="sensor")

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

if fault_pdf and sensor_pdf:
    fault_text = extract_text_from_pdf(fault_pdf)
    sensor_text = extract_text_from_pdf(sensor_pdf)

    st.subheader("Fault Report Content")
    st.text_area("Fault Report", fault_text, height=250)

    st.subheader("Sensor Report Content")
    st.text_area("Sensor Report", sensor_text, height=250)

    # وهنا لاحقًا نضيف المعالجة وتحليل الأعطال تلقائيًا

