### ملف `app.py` (الإصدار المصحح)
```python
import streamlit as st
import pdfplumber
import pandas as pd
import re

st.set_page_config(page_title="أداة تحليل أعطال المركبات", layout="wide")
st.title("أداة تحليل الأعطال وربط الحساسات")

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
    return pd.DataFrame(sensors, columns=['الحساس', 'القراءة'])

code_file = st.file_uploader("تحميل تقرير الأعطال (PDF)", type='pdf')
sensor_file = st.file_uploader("تحميل تقرير الحساسات (PDF)", type='pdf')

if code_file and sensor_file:
    dtc_text = extract_text(code_file)
    sensor_text = extract_text(sensor_file)

    dtcs = extract_dtcs(dtc_text)
    df_dtcs = pd.DataFrame(dtcs, columns=['كود العطل', 'الوصف'])

    df_sensors = extract_sensors(sensor_text)

    st.subheader("أكواد الأعطال المستخرجة")
    st.dataframe(df_dtcs)

    st.subheader("بيانات الحساسات المستخرجة")
    st.dataframe(df_sensors)

    st.subheader("تحليل وربط الحساسات مع الأعطال")
    matched = []
    for _, row in df_dtcs.iterrows():
        for _, srow in df_sensors.iterrows():
            if srow['الحساس'].lower() in row['الوصف'].lower():
                matched.append([
                    row['كود العطل'],
                    row['الوصف'],
                    srow['الحساس'],
                    srow['القراءة'],
                    "العطل مرتبط بالحساس - يرجى التحقق"
                ])

    if matched:
        df_match = pd.DataFrame(matched, columns=["كود العطل", "الوصف", "الحساس", "قراءة الحساس", "تحليل مبدئي"])
        st.success("تم العثور على علاقة بين بعض الأكواد والحساسات:")
        st.dataframe(df_match)
    else:
        st.warning("لا توجد علاقة واضحة بين الأكواد وبيانات الحساسات.")
else:
    st.info("يرجى تحميل تقريري PDF للبدء في المقارنة.")
```
