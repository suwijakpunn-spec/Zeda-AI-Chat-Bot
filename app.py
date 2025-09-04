import streamlit as st
import google.generativeai as genai
import os
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# --- ตั้งค่าหน้าเว็บและ CSS สำหรับ UI ---
st.set_page_config(
    page_title="ZEDA.AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* ปรับปรุงฟอนต์ทั่วทั้งแอป */
body {
    font-family: sans-serif;
}

/* ปรับสีพื้นหลังของหน้าหลักและ sidebar */
.st-emotion-cache-1cypcdb {
    background-color: #000000;
}
.st-emotion-cache-12t9085 {
    background-color: #121212;
    padding-top: 2rem;
}
.st-emotion-cache-13ejs5a {
    background-color: #1C1C1C;
    border-radius: 15px;
    border: none;
    color: white;
}
.st-emotion-cache-10o1a8w {
    background-color: #121212;
}

/* ซ่อนส่วนประกอบของ Streamlit ที่ไม่ต้องการ */
.st-emotion-cache-1aehpbu {
    display: none;
}
.st-emotion-cache-162985f {
    display: none;
}
.st-emotion-cache-j7qwjs {
    display: none;
}
.st-emotion-cache-1v41k9a {
    display: none;
}

/* ปรับแต่ง sidebar */
.st-emotion-cache-1d3744c {
    background-color: #121212;
    color: white;
}
.st-emotion-cache-19p62m1 {
    color: white;
    font-size: 20px;
}
.st-emotion-cache-1ky926a {
    background-color: #212121;
    border-radius: 10px;
}

/* สร้างปุ่มแบบกำหนดเองด้วย HTML/CSS */
.sidebar-button {
    background-color: #212121;
    color: white;
    padding: 12px;
    margin: 5px 0;
    border-radius: 10px;
    text-align: left;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s;
}
.sidebar-button:hover {
    background-color: #333333;
}
</style>
""", unsafe_allow_html=True)

# --- ส่วนของโค้ด AI และการทำงานหลัก ---
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# --- User Authentication ---
try:
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
except FileNotFoundError:
    st.error("ไม่พบไฟล์ config.yaml กรุณาสร้างไฟล์และใส่ข้อมูลตามตัวอย่างที่แนะนำ")
    st.stop()

# แก้ไขการเรียกใช้ Authenticator ให้ถูกต้องตามเวอร์ชันล่าสุด
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# --- สร้างตัวเลือกสำหรับ Login และ Register ---
st.sidebar.title("ZEDA.AI")
st.sidebar.markdown("by **scStudio**")
choice = st.sidebar.radio("เลือกเมนู", ["Login", "Register"])

if choice == "Login":
    st.title("Login")
    # แก้ไขการเรียกใช้ login ให้ถูกต้อง
    name, authentication_status, username = authenticator.login('Login', location='main')
    
    if authentication_status:
        authenticator.logout('Logout', 'sidebar')
        
        # Sidebar
        with st.sidebar:
            st.image("https://i.ibb.co/L50HjHj/ZEDA-AI.png", width=150)
            st.markdown(f"## Welcome, {name}")
            st.markdown("---")
            st.markdown('<div class="sidebar-button">Chat history</div>', unsafe_allow_html=True)
            st.markdown('<div class="sidebar-button">Make my own games</div>', unsafe_allow_html=True)
            st.markdown('<div class="sidebar-button">Code a AI</div>', unsafe_allow_html=True)
            st.markdown('<div class="sidebar-button">Roblox has ban</div>', unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("<p style='font-size: 14px;'>scStudio<br>Free mode</p>", unsafe_allow_html=True)

        # Main content
        col1, col2 = st.columns([1, 6])
        with col1:
            st.markdown("## ZEDA.AI")
        with col2:
            st.markdown("<p style='text-align: right; color: #888;'>zeda0.5</p>", unsafe_allow_html=True)

        # สร้างกล่องแชท
        if "messages" not in st.session_state:
            st.session_state.messages = []
            st.session_state.messages.append({"role": "assistant", "content": "สวัสดีครับ ผมคือ Zeda AI ที่ใช้โมเดลจาก Google มีอะไรให้ผมช่วยไหมครับ?"})
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("type anythings..."):
            prompt_lower = prompt.lower()
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)

            if "your name" in prompt_lower or "ชื่ออะไร" in prompt_lower:
                response_text = "ผมชื่อ Zeda ครับ เป็น AI ที่พัฒนาโดย scStudio และใช้โมเดลจาก Google"
                with st.chat_message("assistant"):
                    st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            else:
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

    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')

elif choice == "Register":
    st.title("Register New User")
    try:
        # แก้ไขการเรียกใช้ register_user ให้ถูกต้อง
        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(
            'Register user',
            preauthorization=False
        )
        if email_of_registered_user:
            st.success('User registered successfully!')
            
            with open('config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
            st.info("โปรดล็อกอินด้วยข้อมูลที่คุณเพิ่งลงทะเบียน")

    except Exception as e:
        st.error(e)

