# now we will start true work


import streamlit as st
import pdfplumber
import pandas as pd
import re
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="Fault Prediction", layout="wide")
st.title("AI Car Diagnosis - Predictive Fault Analysis")

def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text

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
            try:
                deviation = abs(float(value) - float(standard)) / float(standard) * 100 if float(standard) != 0 else 0
            except:
                deviation = None
            sensors.append([name, value, standard, unit, deviation])
    return pd.DataFrame(sensors, columns=["Sensor", "Value", "Standard", "Unit", "Deviation %"])

st.subheader("Upload Sensor Report to Analyze")

sensor_file = st.file_uploader("Upload sensor report (PDF)", type="pdf")

if sensor_file:
    sensor_text = extract_text_from_pdf(sensor_file)
    df_sensors = extract_sensor_data(sensor_text)
    df_sensors.dropna(subset=["Deviation %"], inplace=True)

    st.subheader("Extracted Sensor Data with Deviation")
    st.dataframe(df_sensors)

    # رسم بياني للانحرافات
    st.subheader("Deviation Chart")
    fig, ax = plt.subplots(figsize=(10, 4))
    bars = ax.bar(df_sensors["Sensor"], df_sensors["Deviation %"].astype(float), color="orange")
    ax.set_ylabel("Deviation (%)")
    ax.set_xlabel("Sensor")
    ax.set_title("Sensor Deviation Overview")
    ax.axhline(15, color='red', linestyle='--', label='Critical Deviation Threshold')
    ax.legend()
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

    # عرض الحساسات الخطرة
    high_dev = df_sensors[df_sensors["Deviation %"].astype(float) > 15]
    if not high_dev.empty:
        st.error("Warning: Some sensors show high deviation that may indicate future faults.")
        st.dataframe(high_dev)
    else:
        st.success("All sensor readings are within acceptable deviation limits.")

