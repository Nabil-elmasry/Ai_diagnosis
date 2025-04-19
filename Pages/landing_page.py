
import streamlit as st

st.set_page_config(page_title="Welcome - AI Car Diagnosis", layout="centered")

st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #2c3e50, #ff0000);
        color: white;
    }

    h1 {
        text-align: center;
        font-size: 3em;
        font-family: 'Trebuchet MS', sans-serif;
        color: #ff4b1f;
        text-shadow: 2px 2px 5px #000;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }

    .start-button {
        display: block;
        margin: 30px auto;
        padding: 1em 2.5em;
        font-size: 1.3em;
        font-weight: bold;
        color: white;
        background: linear-gradient(45deg, #ff416c, #ff4b2b);
        border: none;
        border-radius: 12px;
        cursor: pointer;
        box-shadow: 0 0 15px #ff4b2b;
        transition: 0.3s ease;
    }

    .start-button:hover {
        background: linear-gradient(45deg, #ff4b2b, #ff416c);
        transform: scale(1.05);
        box-shadow: 0 0 25px #ff4b2b;
    }

    .footer {
        position: fixed;
        bottom: 15px;
        width: 100%;
        text-align: center;
        font-size: 1.1em;
        color: #f8f8f8;
        font-weight: bold;
        text-shadow: 1px 1px 3px #000;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>AI Car Diagnosis</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='color:white;'>نظام التشخيص الذكي بالذكاء الاصطناعي</h1>", unsafe_allow_html=True)

# زر وهمي للانتقال
st.markdown("""
    <form action="?page=main">
        <button class="start-button" type="submit">ابدأ التشخيص</button>
    </form>
""", unsafe_allow_html=True)

# توقيعك
st.markdown("""
    <div class="footer">
        Eng. Nabil Almasry<br>By AI
    </div>
""", unsafe_allow_html=True)

