# ...โค้ดส่วนอื่น ๆ ของคุณ

# สร้างกล่องแชท
if "messages" not in st.session_state:
    st.session_state.messages = []
    # เพิ่มข้อความต้อนรับของ AI ที่มีชื่อ Zeda
    st.session_state.messages.append({"role": "assistant", "content": "สวัสดีครับ ผมคือ Zeda AI ที่ใช้โมเดลจาก Google มีอะไรให้ผมช่วยไหมครับ?"})

# แสดงข้อความแชทใน History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# รับ Input จากผู้ใช้
if prompt := st.chat_input("type anythings..."):
    # แปลงคำถามให้เป็นตัวพิมพ์เล็กทั้งหมด
    prompt_lower = prompt.lower()

    # เพิ่มข้อความของผู้ใช้ลงใน Session State
    st.session_state.messages.append({"role": "user", "content": prompt})

    # แสดงข้อความของผู้ใช้
    with st.chat_message("user"):
        st.markdown(prompt)

    # ตรวจสอบว่าผู้ใช้ถามชื่อหรือไม่
    if "your name" in prompt_lower or "ชื่ออะไร" in prompt_lower:
        response_text = "ผมชื่อ Zeda ครับ เป็น AI ที่พัฒนาโดย scStudio และใช้โมเดลจาก Google"
        with st.chat_message("assistant"):
            st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
    else:
        # ถ้าไม่ใช่คำถามเกี่ยวกับชื่อ ให้ส่งไปหาโมเดล Gemini
        with st.chat_message("assistant"):
            with st.spinner("กำลังคิดคำตอบ..."):
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
