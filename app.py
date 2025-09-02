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
/* ซ่อนส่วนประกอบของ Streamlit ที่ไม่ต้องการ */
.st-emotion-cache-1cypcdb {
    visibility: hidden;
}
.st-emotion-cache-13ln4jf {
    background-color: #0E1117;
}

/* ปรับแต่ง sidebar */
.st-emotion-cache-12t9085 {
    background-color: #121212;
    padding-top: 5rem;
}
.st-emotion-cache-12t9085 a {
    color: #FAFAFA;
    font-weight: bold;
}
.st-emotion-cache-12t9085 .st-emotion-cache-1ky926a {
    background-color: #262626;
    border-radius: 10px;
}

/* สไตล์กล่องแชท */
.st-emotion-cache-13ejs5a {
    background-color: #212121;
    border-radius: 15px;
    border: none;
}
.st-emotion-cache-1aehpbu {
    background-color: #0E1117;
}
</style>
""", unsafe_allow_html=True)

# --- ส่วนของโค้ด AI และการทำงานหลัก ---
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# Sidebar
with st.sidebar:
    st.image("https://i.ibb.co/L50HjHj/ZEDA-AI.png", use_column_width=True) # เปลี่ยน URL รูปภาพถ้าต้องการ
    st.markdown("## zeda0.5")
    st.markdown("by **scStudio**")
    st.markdown("---")
    st.button("Chat history")
    st.button("Make my own games")
    st.button("Code a AI")
    st.button("Roblox has ban")
    st.markdown("---")
    st.markdown("scStudio<br>Free mode", unsafe_allow_html=True)

# Main content
st.title("ZEDA.AI")
st.markdown("<p style='text-align: right; color: #888;'>zeda0.5</p>", unsafe_allow_html=True)

# สร้างกล่องแชท
if "messages" not in st.session_state:
    st.session_state.messages = []

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

# ตั้งค่า API Key จาก Environment variable
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# กำหนดชื่อเรื่องของแอป
st.title("🤖 แอป AI แชทบอท")

# สร้าง History สำหรับแชท
if "messages" not in st.session_state:
    st.session_state.messages = []

# แสดงข้อความแชทใน History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# รับ Input จากผู้ใช้
if prompt := st.chat_input("คุณมีอะไรอยากถามผมไหม?"):
    # เพิ่มข้อความของผู้ใช้ลงใน Session State
    st.session_state.messages.append({"role": "user", "content": prompt})
    # แสดงข้อความของผู้ใช้
    with st.chat_message("user"):
        st.markdown(prompt)

    # ส่งข้อความไปหา AI
    with st.chat_message("assistant"):
        with st.spinner("กำลังคิดคำตอบ..."):
            try:
                # สร้างประวัติการสนทนา (History) เพื่อให้ AI จดจำ
                messages = [
                    {"role": "user", "parts": [msg["content"]]} if msg["role"] == "user" else 
                    {"role": "model", "parts": [msg["content"]]}
                    for msg in st.session_state.messages
                ]
                
                # ส่งประวัติการสนทนาให้โมเดลเพื่อสร้างคำตอบ
                response = model.generate_content(messages)
                
                # แสดงผลลัพธ์
                st.markdown(response.text)
                
                # เพิ่มข้อความของ AI ลงใน Session State
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
