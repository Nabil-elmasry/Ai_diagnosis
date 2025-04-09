
import streamlit as st
import pdfplumber
import pandas as pd
import re

st.set_page_config(page_title="AI Car Diagnosis", layout="wide")
st.title("AI Car Diagnosis - Unified App")

def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text

def extract_dtcs(text):
    return re.findall(r"(P\d{4})\s+(.+)", text)

def extract_sensor_data(text):
    lines = text.split('\n')
    sensors = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 2:
            name = ' '.join(parts[:-1])
            try:
                value = float(parts[-1])
            except ValueError:
                value = parts[-1]
            sensors.append([name, value])
    return pd.DataFrame(sensors, columns=["Sensor", "Value"])

# Ø±ÙØ¹ Ø§Ù„Ù…Ù„ÙØ§Øª
sensor_file = st.file_uploader("Upload Sensor Report (PDF)", type="pdf")
code_file = st.file_uploader("Upload Fault Report (PDF)", type="pdf")

if sensor_file and code_file:
    # Ø§Ø³ØªØ®Ø±Ø§Ø¬ Ø§Ù„Ù†ØµÙˆØµ
    sensor_text = extract_text_from_pdf(sensor_file)
    code_text = extract_text_from_pdf(code_file)

    # Ø§Ø³ØªØ®Ø±Ø§Ø¬ Ø§Ù„Ø¨ÙŠØ§Ù†Ø§Øª
    df_sensors = extract_sensor_data(sensor_text)
    dtcs = extract_dtcs(code_text)
    df_dtcs = pd.DataFrame(dtcs, columns=["Code", "Description"])

    # Ø¹Ø±Ø¶ Ø§Ù„Ø¬Ø¯Ø§ÙˆÙ„
    st.subheader("1. Extracted Sensor Data")
    st.dataframe(df_sensors)

    st.subheader("2. Extracted Fault Codes")
    st.dataframe(df_dtcs)

    # Ø§Ù„Ù…Ù‚Ø§Ø±Ù†Ø© ÙˆØ§Ù„Ø±Ø¨Ø·
    st.subheader("3. Matching Analysis")
    matches = []
    for _, dtc_row in df_dtcs.iterrows():
        for _, sensor_row in df_sensors.iterrows():
            if sensor_row["Sensor"].lower() in dtc_row["Description"].lower():
                matches.append([
                    dtc_row["Code"],
                    dtc_row["Description"],
                    sensor_row["Sensor"],
                    sensor_row["Value"],
                    "Ø§Ù„Ø¹Ø·Ù„ Ù…Ø±ØªØ¨Ø· Ø¨Ø§Ù„Ø­Ø³Ø§Ø³ - ÙŠØ±Ø¬Ù‰ Ø§Ù„ØªØ­Ù‚Ù‚"
                ])

    if matches:
        df_matches = pd.DataFrame(matches, columns=["ÙƒÙˆØ¯ Ø§Ù„Ø¹Ø·Ù„", "Ø§Ù„ÙˆØµÙ", "Ø§Ù„Ø­Ø³Ø§Ø³", "Ø§Ù„Ù‚ÙŠÙ…Ø©", "ØªØ­Ù„ÙŠÙ„ Ù…Ø¨Ø¯Ø¦ÙŠ"])
        st.success("ØªÙ… Ø§Ù„Ø¹Ø«ÙˆØ± Ø¹Ù„Ù‰ Ø¹Ù„Ø§Ù‚Ø© Ø¨ÙŠÙ† Ø¨Ø¹Ø¶ Ø§Ù„Ø£ÙƒÙˆØ§Ø¯ ÙˆØ§Ù„Ø­Ø³Ø§Ø³Ø§Øª:")
        st.table(df_matches)
    else:
        st.info("Ù„Ø§ ØªÙˆØ¬Ø¯ Ø¹Ù„Ø§Ù‚Ø© Ù…Ø¨Ø§Ø´Ø±Ø© Ø¨ÙŠÙ† Ø§Ù„Ø­Ø³Ø§Ø³Ø§Øª ÙˆØ£ÙˆØµØ§Ù Ø§Ù„Ø£Ø¹Ø·Ø§Ù„.")
else:
    st.warning("ÙŠØ±Ø¬Ù‰ Ø±ÙØ¹ ÙƒÙ„Ø§ Ø§Ù„ØªÙ‚Ø±ÙŠØ±ÙŠÙ† Ù„Ø¨Ø¯Ø¡ Ø§Ù„ØªØ­Ù„ÙŠÙ„.")