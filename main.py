
import streamlit as st

st.set_page_config(page_title="AI Diagnosis")

st.sidebar.title("قائمة التنقل")
st.sidebar.page_link("pages/landing.py", label="الصفحة الافتتاحية")
st.sidebar.page_link("pages/diagnosis.py", label="تحليل الأعطال")

st.markdown("### من فضلك اختر صفحة من القائمة الجانبية.")
