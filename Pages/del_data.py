
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Reset Data", layout="wide")
st.title("Clear Data File - car_analysis_data.csv")

st.warning("Use this only ONCE if you want to reset all your stored sensor data!")

if st.button("Clear CSV Data and Keep Headers"):
    try:
        df = pd.read_csv("car_analysis_data.csv")
        headers = list(df.columns)
        pd.DataFrame(columns=headers).to_csv("car_analysis_data.csv", index=False)
        st.success("CSV data cleared. Headers preserved.")
    except Exception as e:
        st.error(f"Error clearing data: {e}")

