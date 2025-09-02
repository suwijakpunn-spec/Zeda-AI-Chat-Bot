import streamlit as st
import google.generativeai as genai
import os

# --- การตั้งค่าทั่วไปของหน้าเว็บ ---
st.set_page_config(
    page_title="ZEDA.AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- โค้ด CSS สำหรับปรับแต่งหน้าตา ---
st.markdown("""
<style>
/* ปรับสีพื้นหลังของหน้าหลักและ Sidebar */
.st-emotion-cache-13ln4jf {
    background-color: #000000; /* สีพื้นหลังหลัก */
}
.st-emotion-cache-12t9085 {
    background-color: #121212; /* สี Sidebar */
    padding-top: 5rem;
}

/* ซ่อนส่วนประกอบของ Streamlit ที่ไม่ต้องการ */
.st-emotion-cache-162985f {
    visibility: hidden;
}

/* ปรับแต่งกล่องแชท */
.st-emotion-cache-1n1j115 {
    background-color: #212121;
    border-radius: 15px;
    border: none;
}
.st-emotion-cache-1aehpbu {
    background-color: #0E1117;
}

/* ปรับแต่งปุ่มใน Sidebar */
.sidebar .stButton>button {
    background-color: #262626;
    border: none;
    color: white;
    padding: 10px 24px;
    text-align: left;
    display: block;
    width: 100%;
    margin-bottom: 8px;
    border-radius: 10px;
    font-size: 16px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# --- ส่วนของโค้ด AI และการทำงานหลัก ---
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# Sidebar
with st.sidebar:
    st.image("https://i.ibb.co/L50HjHj/ZEDA-AI.png", use_column_width=True) # URL รูปภาพโลโก้
    st.markdown("## zeda0.5")
    st.markdown("by **scStudio**")
    st.markdown("---")
    st.button("Chat history", key="chat_history_btn")
    st.button("Make my own games", key="make_games_btn")
    st.button("Code a AI", key="code_ai_btn")
    st.button("Roblox has ban", key="roblox_ban_btn")
    st.markdown("---")
    st.markdown("scStudio<br>Free mode", unsafe_allow_html=True)

# Main content
col1, col2 = st.columns([1, 6])
with col1:
    st.markdown("## ZEDA.AI")
with col2:
    st.markdown("<p style='text-align: right; color: #888;'>zeda0.5</p>", unsafe_allow_html=True)

# สร้างกล่องแชท
if "messages" not in st.session_state:
    st.session_state.messages = []
    # เพิ่มข้อความต้อนรับของ AI ที่มีชื่อ Zeda
    st.session_state.messages.append({"role": "assistant", "content": "สวัสดีครับ ผมคือ Zeda AI ที่ใช้โมเดลจาก Google มีอะไรให้ผมช่วยไหมครับ?"})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("type anythings..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Loading..."):
            try:
                messages = [
                    {"role": "user", "parts": [msg["content"]]} if msg["role"] == "user" else
                    {"role": "model", "parts": [msg["content"]]}
                    for msg in st.session_state.messages
                ]
                response = model.generate_content(messages)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")

