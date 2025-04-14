#need to save
import streamlit as st
import pdfplumber
import pandas as pd
import re
import os

st.set_page_config(page_title="AI Car Diagnosis", layout="wide")
st.title("AI Car Diagnosis - Mobile-Friendly Sensor Upload")

# دالة قراءة نص PDF
def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = ""
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text

# استخراج الأكواد
def extract_dtcs(text):
    return re.findall(r"(P\d{4})\s+(.+)", text)

# استخراج بيانات الحساسات
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

# تخزين مؤقت للملفات
if "sensor_reports" not in st.session_state:
    st.session_state.sensor_reports = []

st.subheader("Step 1: Add Sensor Report (واحد فقط في كل مرة)")

sensor_file = st.file_uploader("Upload one sensor report (PDF)", type="pdf")

if sensor_file and st.button("Add to Sensor List"):
    st.session_state.sensor_reports.append(sensor_file)
    st.success(f"Added report: {sensor_file.name}")

st.write(f"Total uploaded sensor reports: {len(st.session_state.sensor_reports)}")

st.subheader("Step 2: Upload Fault Code Report")
code_file = st.file_uploader("Upload fault report (PDF)", type="pdf")

# زر التحليل والإعادة
analyze = st.button("Analyze All Reports")
reset = st.button("Reset Sensor Reports")

if reset:
    st.session_state.sensor_reports = []
    st.success("Sensor reports list has been reset.")

if analyze:
    if not st.session_state.sensor_reports:
        st.warning("Please upload at least one sensor report.")
    elif not code_file:
        st.warning("Please upload the fault code report.")
    else:
        # دمج كل النصوص من الحساسات
        sensor_text = ""
        for file in st.session_state.sensor_reports:
            sensor_text += extract_text_from_pdf(file)

        code_text = extract_text_from_pdf(code_file)

        df_sensors = extract_sensor_data(sensor_text)
        dtcs = extract_dtcs(code_text)
        df_dtcs = pd.DataFrame(dtcs, columns=["Code", "Description"])

        st.subheader("1. Extracted Sensor Data")
        st.dataframe(df_sensors)

        st.subheader("2. Extracted Fault Codes")
        st.dataframe(df_dtcs)

        st.subheader("3. Sensor-Fault Matching & Deviation Analysis")
        matches = []
        for _, dtc_row in df_dtcs.iterrows():
            for _, sensor_row in df_sensors.iterrows():
                if sensor_row["Sensor"].lower() in dtc_row["Description"].lower():
                    try:
                        value = float(sensor_row["Value"])
                        standard = float(sensor_row["Standard"])
                        deviation_percent = abs(value - standard) / standard * 100 if standard != 0 else 0
                        status = "High Deviation" if deviation_percent > 15 else "OK"
                    except:
                        deviation_percent = "N/A"
                        status = "Cannot Evaluate"

                    matches.append([
                        dtc_row["Code"],
                        dtc_row["Description"],
                        sensor_row["Sensor"],
                        sensor_row["Value"],
                        sensor_row["Standard"],
                        sensor_row["Unit"],
                        f"{deviation_percent:.1f}%" if isinstance(deviation_percent, float) else deviation_percent,
                        status
                    ])

        if matches:
            df_matches = pd.DataFrame(matches, columns=[
                "Code", "Fault Description", "Sensor", "Value", "Standard", "Unit", "Deviation %", "Status"
            ])
            st.success("Sensor deviation analysis completed:")
            st.dataframe(df_matches)
        else:
            st.info("No direct match or deviation detected.")

        # حفظ البيانات في CSV
        try:
            sensor_dict = {row['Sensor']: row['Value'] for _, row in df_sensors.iterrows()}
            sensor_dict['Fault Codes'] = ','.join(df_dtcs['Code'].tolist())

            new_case_df = pd.DataFrame([sensor_dict])

            csv_filename = "car_analysis_data.csv"
            if os.path.exists(csv_filename):
                existing_df = pd.read_csv(csv_filename)
                final_df = pd.concat([existing_df, new_case_df], ignore_index=True)
            else:
                final_df = new_case_df

            final_df.to_csv(csv_filename, index=False)
            st.success("Data saved successfully to car_analysis_data.csv")

            with open(csv_filename, "rb") as f:
                st.download_button(
                    label="Download car_analysis_data.csv",
                    data=f,
                    file_name="car_analysis_data.csv",
                    mime="text/csv"
                )

            # إعادة تعيين قائمة الحساسات بعد التحليل
            st.session_state.sensor_reports = []

        except Exception as e:
            st.error(f"Error saving data: {e}")

