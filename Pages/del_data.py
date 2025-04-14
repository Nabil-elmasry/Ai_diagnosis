
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Reset Data", layout="wide")
st.title("Clear Data File - car_analysis_data.csv")

st.warning("Use this only ONCE if you want to reset all your stored sensor data!")

# اضغط الزر مرة واحدة بس لتفريغ البيانات مع الحفاظ على الهيكل
if st.button("Clear CSV Data and Keep Headers"):
    try:
        # إذا الملف موجود، ناخد أسماء الأعمدة الأصلية
        if os.path.exists("car_analysis_data.csv"):
            df = pd.read_csv("car_analysis_data.csv")
            headers = list(df.columns)
        else:
            # لو أول مرة تشغله، نبدأ بهيكل افتراضي (تقدر تعدله لاحقًا)
            headers = ["Sensor1", "Sensor2", "Sensor3", "Fault Codes"]

        # نكتب ملف جديد بنفس العناوين، بدون بيانات
        pd.DataFrame(columns=headers).to_csv("car_analysis_data.csv", index=False)
        st.success("CSV file reset successfully. You can now start adding real data.")

    except Exception as e:
        st.error(f"Error resetting file: {e}")
