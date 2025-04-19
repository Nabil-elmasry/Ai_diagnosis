
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Welcome - AI Car Diagnosis", layout="centered")

# === تصميم الخلفية والألوان ===
st.markdown("""
    <style>
    body {
        background-color: #0F2027;
        background-image: linear-gradient(to right, #2C5364, #203A43, #0F2027);
        color: white;
    }
    .centered {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 90vh;
        text-align: center;
    }
    .start-button {
        margin-top: 30px;
        padding: 0.75em 2em;
        font-size: 1.2em;
        background-color: #00c9a7;
        color: white;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        transition: 0.3s;
    }
    .start-button:hover {
        background-color: #02b393;
    }
    .footer {
        position: fixed;
        bottom: 10px;
        width: 100%;
        text-align: center;
        font-weight: bold;
        color: #CCCCCC;
        font-size: 0.9em;
    }
    </style>
""", unsafe_allow_html=True)

# === عرض المحتوى ===
st.markdown("""
<div class="centered">
    <h1>Welcome to</h1>
    <h1 style='color:#00c9a7'>AI Car Diagnosis System</h1>
    <p>Smart predictive maintenance & fault analysis powered by AI</p>
    <form action="?page=main">
        <button class="start-button" type="submit">ابدأ التشخيص</button>
    </form>
</div>
<div class="footer">
    Eng. Nabil Almasry<br>By AI
</div>
""", unsafe_allow_html=True)
