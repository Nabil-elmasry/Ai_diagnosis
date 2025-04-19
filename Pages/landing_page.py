
import streamlit as st

st.set_page_config(page_title="Welcome - AI Car Diagnosis", layout="centered")

# ====== التصميم ======
st.markdown("""
<style>
body {
    background-color: #000428;
    background-image: linear-gradient(to right, #004e92, #000428);
}

h1 {
    color: #00ffcc;
    text-align: center;
    font-size: 3em;
    font-family: 'Trebuchet MS', sans-serif;
    margin-bottom: 0.2em;
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
  from {
    text-shadow: 0 0 10px #00ffcc, 0 0 20px #00ffcc;
  }
  to {
    text-shadow: 0 0 20px #00ffff, 0 0 30px #00ffff;
  }
}

button.start-button {
    background: linear-gradient(to right, #00c9ff, #92fe9d);
    border: none;
    padding: 1em 2.5em;
    font-size: 1.3em;
    border-radius: 12px;
    cursor: pointer;
    color: black;
    font-weight: bold;
    margin-top: 2em;
    transition: transform 0.3s ease;
}
button.start-button:hover {
    transform: scale(1.05);
    background: linear-gradient(to right, #1cd8d2, #93edc7);
}

.footer {
    position: fixed;
    bottom: 15px;
    width: 100%;
    text-align: center;
    font-size: 1.1em;
    color: #cccccc;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ====== المحتوى ======
st.markdown("<h1>AI Car Diagnosis</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='color:#fff;'>نظام التشخيص الذكي</h1>", unsafe_allow_html=True)

# ====== زر الدخول ======
st.markdown("""
    <form action="?page=main">
        <button class="start-button" type="submit">ابدأ التشخيص</button>
    </form>
""", unsafe_allow_html=True)

# ====== التوقيع ======
st.markdown("""
<div class="footer">
    Eng. Nabil Almasry<br>By AI
</div>
""", unsafe_allow_html=True)

