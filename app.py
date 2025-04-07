
import streamlit as st
import pdfplumber
import pandas as pd
import re

def extract_sensor_data(text):
    pattern = r"(?P<Name>[\w\s\-/()#]+?)\s+(?P<Value>[\d\-.]+)\s+(?P<Range>[\d\- .]+)\s+(?P<Unit>[\w/%Â°]+)"
    matches = re.findall(pattern, text)
    data = []
    for match in matches:
        data.append({
            "Name": match[0].strip(),
            "Value": float(match[1]),
            "Range": match[2].strip(),
            "Unit": match[3].strip()
        })
    return pd.DataFrame(data)

def main():
    st.title("AI Car Diagnosis")

    sensor_file = st.file_uploader("Ø§Ø±ÙØ¹ ØªÙ‚Ø±ÙŠØ± Ø§Ù„Ø­Ø³Ø§Ø³Ø§Øª (sensor)", type="pdf")
    code_file = st.file_uploader("Ø§Ø±ÙØ¹ ØªÙ‚Ø±ÙŠØ± Ø§Ù„Ø£Ø¹Ø·Ø§Ù„ (code)", type="pdf")

    if sensor_file is not None:
        with pdfplumber.open(sensor_file) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
            df = extract_sensor_data(text)

            def highlight_range(row):
                try:
                    min_val, max_val = map(float, row['Range'].split('-'))
                    if row['Value'] < min_val or row['Value'] > max_val:
                        return ['background-color: red']*len(row)
                    else:
                        return ['background-color: #c6f6d5']*len(row)
                except:
                    return ['']*len(row)

            st.subheader("Ø¨ÙŠØ§Ù†Ø§Øª Ø§Ù„Ø­Ø³Ø§Ø³Ø§Øª")
            st.dataframe(df.style.apply(highlight_range, axis=1))

    if code_file is not None:
        with pdfplumber.open(code_file) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
            st.subheader("Ø£ÙƒÙˆØ§Ø¯ Ø§Ù„Ø£Ø¹Ø·Ø§Ù„")
            dtcs = re.findall(r"(P\d{4})\s+(.*?)(?:Current|History|Pending)?", text)
            code_df = pd.DataFrame(dtcs, columns=["DTC Code", "Description"])
            st.table(code_df)

if __name__ == "__main__":
    main()