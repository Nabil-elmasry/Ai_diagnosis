
import streamlit as st
import pdfplumber
import pandas as pd
import re

st.set_page_config(page_title="Diagnosis Comparison", layout="wide")
st.title("ØªØ´Ø®ÙŠØµ Ø§Ù„Ø£Ø¹Ø·Ø§Ù„ Ø¨Ù…Ù‚Ø§Ø±Ù†Ø© ØªÙ‚Ø±ÙŠØ± Ø§Ù„ÙØ­Øµ ÙˆÙ‚Ø±Ø§Ø¡Ø§Øª Ø§Ù„Ø­Ø³Ø§Ø³Ø§Øª")

def extract_text(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

def extract_dtcs(text):
    return re.findall(r'(P\d{4})\s+(.+)', text)

def extract_sensors(text):
    lines = text.split('\n')
    sensors = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 2:
            name = ' '.join(parts[:-1])
            value = parts[-1]
            sensors.append([name, value])
    return pd.DataFrame(sensors, columns=['Ø§Ù„Ø­Ø³Ø§Ø³', 'Ø§Ù„Ù‚ÙŠÙ…Ø©'])

code_file = st.file_uploader("Ø§Ø±ÙØ¹ ØªÙ‚Ø±ÙŠØ± Ø§Ù„Ø£Ø¹Ø·Ø§Ù„ (PDF)", type='pdf')
sensor_file = st.file_uploader("Ø§Ø±ÙØ¹ ØªÙ‚Ø±ÙŠØ± Ø§Ù„Ø­Ø³Ø§Ø³Ø§Øª (PDF)", type='pdf')

if code_file and sensor_file:
    dtc_text = extract_text(code_file)
    sensor_text = extract_text(sensor_file)

    dtcs = extract_dtcs(dtc_text)
    df_dtcs = pd.DataFrame(dtcs, columns=['Ø§Ù„ÙƒÙˆØ¯', 'Ø§Ù„ÙˆØµÙ'])

    df_sensors = extract_sensors(sensor_text)

    st.subheader("Ø£ÙƒÙˆØ§Ø¯ Ø§Ù„Ø£Ø¹Ø·Ø§Ù„")
    st.dataframe(df_dtcs)

    st.subheader("Ø¨ÙŠØ§Ù†Ø§Øª Ø§Ù„Ø­Ø³Ø§Ø³Ø§Øª")
    st.dataframe(df_sensors)

    # Ù…Ù‚Ø§Ø±Ù†Ø© Ù…Ø¨Ø³Ø·Ø©: Ø¹Ø±Ø¶ Ø§Ù„Ø­Ø³Ø§Ø³Ø§Øª Ø§Ù„ØªÙŠ ÙŠØ¸Ù‡Ø± Ø§Ø³Ù…Ù‡Ø§ Ø¶Ù…Ù† ÙˆØµÙ Ø§Ù„ÙƒÙˆØ¯
    st.subheader("Ù…Ù‚Ø§Ø±Ù†Ø© ÙˆØªØ­Ù„ÙŠÙ„ Ø£ÙˆÙ„ÙŠ")
    matched = []
    for _, row in df_dtcs.iterrows():
        for _, srow in df_sensors.iterrows():
            if srow['Ø§Ù„Ø­Ø³Ø§Ø³'].lower() in row['Ø§Ù„ÙˆØµÙ'].lower():
                matched.append([row['Ø§Ù„ÙƒÙˆØ¯'], row['Ø§Ù„ÙˆØµÙ'], srow['Ø§Ù„Ø­Ø³Ø§Ø³'], srow['Ø§Ù„Ù‚ÙŠÙ…Ø©']])

    if matched:
        df_match = pd.DataFrame(matched, columns=["Ø§Ù„ÙƒÙˆØ¯", "ÙˆØµÙ Ø§Ù„Ø¹Ø·Ù„", "Ø§Ù„Ø­Ø³Ø§Ø³ Ø§Ù„Ù…Ø±ØªØ¨Ø·", "Ù‚ÙŠÙ…Ø© Ø§Ù„Ø­Ø³Ø§Ø³"])
        st.success("ØªÙ… Ø§Ù„Ø¹Ø«ÙˆØ± Ø¹Ù„Ù‰ Ø¹Ù„Ø§Ù‚Ø§Øª Ø¨ÙŠÙ† Ø§Ù„Ø£ÙƒÙˆØ§Ø¯ ÙˆØ§Ù„Ø­Ø³Ø§Ø³Ø§Øª:")
        st.dataframe(df_match)
    else:
        st.warning("Ù„Ù… ÙŠØªÙ… Ø§Ù„Ø¹Ø«ÙˆØ± Ø¹Ù„Ù‰ Ø¹Ù„Ø§Ù‚Ø© ÙˆØ§Ø¶Ø­Ø© Ø¨ÙŠÙ† Ø§Ù„Ø£ÙƒÙˆØ§Ø¯ ÙˆÙ‚Ø±Ø§Ø¡Ø§Øª Ø§Ù„Ø­Ø³Ø§Ø³Ø§Øª.")
else:
    st.info("Ù…Ù† ÙØ¶Ù„Ùƒ Ø§Ø±ÙØ¹ ÙƒÙ„Ø§ Ø§Ù„ØªÙ‚Ø±ÙŠØ±ÙŠÙ† Ù„Ù„Ø¨Ø¯Ø¡ Ø¨Ø§Ù„Ù…Ù‚Ø§Ø±Ù†Ø©.")