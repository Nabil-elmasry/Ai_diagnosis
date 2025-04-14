#final del
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Reset CSV Data", layout="wide")
st.title("إعادة ضبط ملف البيانات - car_analysis_data.csv")

st.info("استخدم هذا الزر مرة واحدة فقط لمسح البيانات القديمة مع الاحتفاظ بأسماء الأعمدة.")

# الزر الوحيد لإعادة التهيئة
if st.button("تفريغ البيانات (الاحتفاظ بالعناوين فقط)"):
    try:
        csv_path = "car_analysis_data.csv"

        # لو الملف موجود، نأخذ العناوين
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            headers = df.columns.tolist()
        else:
            # لو الملف مش موجود، نجهزه بعناوين افتراضية (تقدر تعدلها لاحقًا)
            headers = ["Sensor1", "Sensor2", "Sensor3", "Fault Codes"]

        # نحفظ الملف بالعناوين فقط بدون بيانات
        pd.DataFrame(columns=headers).to_csv(csv_path, index=False)
        st.success("تم مسح البيانات بنجاح مع الاحتفاظ بأسماء الأعمدة.")
    except Exception as e:
        st.error(f"حدث خطأ أثناء إعادة الضبط: {e}")
