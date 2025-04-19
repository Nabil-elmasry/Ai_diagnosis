
import streamlit as st

st.set_page_config(page_title="AI Car Diagnosis", layout="centered")

# ======= تنسيق بصري مميز ومتدرج بالأحمر والأزرق مع تأثيرات متحركة =======
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #1f1c2c, #928DAB);
    }
    h1 {
        text-align: center;
        font-size: 3em;
        font-family: 'Arial Black', sans-serif;
        color: #FF4B2B;
        animation: pulse 2s infinite;
        text-shadow: 2px 2px 10px #000;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.03); }
        100% { transform: scale(1); }
    }
    .start-button {
        display: block;
        margin: 40px auto;
        padding: 1em 2.5em;
        font-size: 1.2em;
        font-weight: bold;
        background: linear-gradient(45deg, #FF416C, #FF4B2B);
        color: white;
        border: none;
        border-radius: 12px;
        box-shadow: 0 0 15px #FF4B2B;
        cursor: pointer;
        transition: 0.3s ease;
    }
    .start-button:hover {
        transform: scale(1.08);
        background: linear-gradient(45deg, #ff4b2b, #ff416c);
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

# ======= العنوان الرئيسي =======
st.markdown("<h1>AI Car Diagnosis System</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='color:white;'>نظام التشخيص الذكي بالذكاء الاصطناعي</h1>", unsafe_allow_html=True)

# ======= زر الانتقال للصفحة التالية =======
st.markdown("""
    <form action="/?page=diagnosis">
        <button class="start-button" type="submit">ابدأ التشخيص</button>
    </form>
""", unsafe_allow_html=True)

# ======= توقيع Eng. Nabil =======
st.markdown("""
    <div class="footer">
        Eng. Nabil Almasry<br>By AI
    </div>
""", unsafe_allow_html=True)

