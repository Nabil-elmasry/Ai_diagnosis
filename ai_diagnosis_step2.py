
import streamlit as st
import pdfplumber
import pandas as pd
import re

st.set_page_config(page_title="AI Car Diagnosis", layout="wide")
st.title("AI Car Diagnosis - Enhanced Sensor Analysis")

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
        if len(parts) >= 4:
            name = ' '.join(parts[:-3])
            value = parts[-3]
            standard = parts[-2]
            unit = parts[-1]
            sensors.append([name, value, standard, unit])
    return pd.DataFrame(sensors, columns=["Sensor", "Value", "Standard", "Unit"])

# Upload files
sensor_file = st.file_uploader("Upload Sensor Report (PDF)", type="pdf")
code_file = st.file_uploader("Upload Fault Report (PDF)", type="pdf")

if sensor_file and code_file:
    sensor_text = extract_text_from_pdf(sensor_file)
    code_text = extract_text_from_pdf(code_file)

    df_sensors = extract_sensor_data(sensor_text)
    dtcs = extract_dtcs(code_text)
    df_dtcs = pd.DataFrame(dtcs, columns=["Code", "Description"])

    st.subheader("1. Extracted Sensor Data")
    st.dataframe(df_sensors)

    st.subheader("2. Extracted Fault Codes")
    st.dataframe(df_dtcs)

    st.subheader("3. Sensor-Fault Matching Analysis")
    matches = []
    for _, dtc_row in df_dtcs.iterrows():
        for _, sensor_row in df_sensors.iterrows():
            if sensor_row["Sensor"].lower() in dtc_row["Description"].lower():
                try:
                    value = float(sensor_row["Value"])
                    standard = float(sensor_row["Standard"])
                    deviation = abs(value - standard)
                    status = "High Deviation" if deviation > 10 else "Within Range"
                except:
                    status = "Cannot Evaluate"

                matches.append([
                    dtc_row["Code"],
                    dtc_row["Description"],
                    sensor_row["Sensor"],
                    sensor_row["Value"],
                    sensor_row["Standard"],
                    sensor_row["Unit"],
                    status
                ])

    if matches:
        df_matches = pd.DataFrame(matches, columns=["Code", "Fault Description", "Sensor", "Value", "Standard", "Unit", "Evaluation"])
        st.success("Match found with sensor deviation analysis:")
        st.dataframe(df_matches)
    else:
        st.info("No direct match or deviation found.")
else:
    st.warning("Please upload both sensor and fault PDF reports to proceed.")

