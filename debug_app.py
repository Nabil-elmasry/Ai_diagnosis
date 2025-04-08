
### ملف `debug_app.py`
```python
import streamlit as st
import pdfplumber

st.set_page_config(page_title="عرض البيانات الخام", layout="wide")
st.title("عرض البيانات الخام لتقارير الأعطال والحساسات")

def extract_text(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

# رفع الملفات
code_file = st.file_uploader("تحميل تقرير الأعطال (PDF)", type="pdf")
sensor_file = st.file_uploader("تحميل تقرير الحساسات (PDF)", type="pdf")

if code_file:
    st.subheader("النص الخام لتقرير الأعطال (أول 50 سطرًا)")
    fault_text = extract_text(code_file)
    lines = fault_text.split("\n")
    preview = "\n".join(lines[:50]) if len(lines) > 50 else fault_text
    st.text(preview)

if sensor_file:
    st.subheader("النص الخام لتقرير الحساسات (أول 50 سطرًا)")
    sensor_text = extract_text(sensor_file)
    lines = sensor_text.split("\n")
    preview = "\n".join(lines[:50]) if len(lines) > 50 else sensor_text
    st.text(preview)

if not code_file and not sensor_file:
    st.info("يرجى تحميل تقرير واحد على الأقل لعرض محتواه الخام.")
```
