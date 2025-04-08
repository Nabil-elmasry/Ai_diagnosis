
import streamlit as st
import pdfplumber

st.set_page_config(page_title="Diagnosis Debug View", layout="wide")
st.title("Raw Data Debug - Fault & Sensor Reports")

def extract_text(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

# رفع الملفات
code_file = st.file_uploader("Upload Fault Report (PDF)", type="pdf")
sensor_file = st.file_uploader("Upload Sensor Report (PDF)", type="pdf")

if code_file:
    st.subheader("Raw Fault Report Text (First 50 lines)")
    fault_text = extract_text(code_file)
    lines = fault_text.split("\n")
    preview = "\n".join(lines[:50]) if len(lines) > 50 else fault_text
    st.text(preview)

if sensor_file:
    st.subheader("Raw Sensor Report Text (First 50 lines)")
    sensor_text = extract_text(sensor_file)
    lines = sensor_text.split("\n")
    preview = "\n".join(lines[:50]) if len(lines) > 50 else sensor_text
    st.text(preview)

if not code_file and not sensor_file:
    st.info("Please upload at least one PDF report to preview its raw contents.")
