import streamlit as st
import google.generativeai as genai
import os

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