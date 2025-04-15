
import streamlit as st
import pdfplumber
import pandas as pd
import re
import plotly.express as px

st.set_page_config(page_title="Smart Prediction", layout="wide")
st.title("AI Predictive Maintenance - Sensor Deviation Dashboard")

# --- دوال المساعدة ---
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
            sensors.append([name, float(value), float(standard), unit, deviation])
    return pd.DataFrame(sensors, columns=["Sensor", "Value", "Standard", "Unit", "Deviation %"])

# --- واجهة المستخدم ---
sensor_file = st.file_uploader("Upload Sensor Report (PDF)", type="pdf")

if sensor_file:
    text = extract_text_from_pdf(sensor_file)
    df = extract_sensor_data(text)
    df.dropna(subset=["Deviation %"], inplace=True)

    st.subheader("1. Extracted Sensor Data")
    st.dataframe(df)

    # --- رسم بياني متطور ---
    st.subheader("2. Sensor Deviation Visualization")

    df["Status"] = df["Deviation %"].apply(
        lambda d: "OK" if d <= 10 else "Warning" if d <= 15 else "Critical"
    )

    color_map = {
        "OK": "green",
        "Warning": "orange",
        "Critical": "red"
    }

    fig = px.bar(
        df,
        x="Sensor",
        y="Deviation %",
        color="Status",
        color_discrete_map=color_map,
        text="Deviation %",
        title="Deviation Levels per Sensor",
        animation_frame="Status",
        range_y=[0, max(df["Deviation %"].max(), 20) + 5]
    )

    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(xaxis_tickangle=-45, height=500)
    st.plotly_chart(fig, use_container_width=True)

    # --- تنبيه للحساسات الحرجة ---
    st.subheader("3. Critical Sensors Summary")
    critical = df[df["Status"] == "Critical"]
    if not critical.empty:
        st.error("Sensors with Critical Deviation Found:")
        st.dataframe(critical)
    else:
        st.success("No critical deviations detected.")

    # --- حفظ اختياري للبيانات لاحقًا ---
    st.info("سيتم قريبًا ربط هذا التحليل بالنموذج الذكي للتنبؤ بالعطل بناءً على قراءات الحساسات.")

else:
    st.warning("يرجى رفع ملف PDF يحتوي على قراءات الحساسات لبدء التحليل.")
