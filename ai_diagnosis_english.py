
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

# Upload files
sensor_file = st.file_uploader("Upload Sensor Report (PDF)", type="pdf")
code_file = st.file_uploader("Upload Fault Report (PDF)", type="pdf")

if sensor_file and code_file:
    # Extract text
    sensor_text = extract_text_from_pdf(sensor_file)
    code_text = extract_text_from_pdf(code_file)

    # Extract data
    df_sensors = extract_sensor_data(sensor_text)
    dtcs = extract_dtcs(code_text)
    df_dtcs = pd.DataFrame(dtcs, columns=["Code", "Description"])

    # Display tables
    st.subheader("1. Extracted Sensor Data")
    st.dataframe(df_sensors)

    st.subheader("2. Extracted Fault Codes")
    st.dataframe(df_dtcs)

    # Matching
    st.subheader("3. Sensor-Fault Matching Analysis")
    matches = []
    for _, dtc_row in df_dtcs.iterrows():
        for _, sensor_row in df_sensors.iterrows():
            if sensor_row["Sensor"].lower() in dtc_row["Description"].lower():
                matches.append([
                    dtc_row["Code"],
                    dtc_row["Description"],
                    sensor_row["Sensor"],
                    sensor_row["Value"],
                    "Possibly related sensor issue - check sensor condition"
                ])

    if matches:
        df_matches = pd.DataFrame(matches, columns=["Code", "Fault Description", "Sensor", "Sensor Value", "Analysis"])
        st.success("Match found between some fault codes and sensor readings:")
        st.dataframe(df_matches)
    else:
        st.info("No clear relation found between fault codes and sensor readings.")
else:
    st.warning("Please upload both sensor and fault PDF reports to proceed.")