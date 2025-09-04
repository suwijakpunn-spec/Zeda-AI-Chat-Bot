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

# --- CSS ส่วนที่เหลือของคุณ ---
st.markdown("""
<style>
/* ... CSS ของคุณ ... */
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
    st.error("ไม่พบไฟล์ config.yaml กรุณาตรวจสอบว่าคุณสร้างไฟล์และใส่ข้อมูลอย่างถูกต้อง")
    st.stop() # หยุดการทำงานหากไม่มีไฟล์ config

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# --- สร้างตัวเลือกสำหรับ Login และ Register ---
choice = st.sidebar.selectbox("เลือกเมนู", ["Login", "Register"])

if choice == "Login":
    st.title("Login")
    name, authentication_status, username = authenticator.login('Login')
    
    if authentication_status:
        authenticator.logout('Logout', 'sidebar')

        # Sidebar และเนื้อหาหลักที่แสดงหลังจากล็อกอินสำเร็จ
        # ... (โค้ดส่วนที่คุณมีอยู่แล้ว) ...
        with st.sidebar:
            st.image("https://i.ibb.co/L50HjHj/ZEDA-AI.png", width=150)
            st.markdown(f"## Welcome, {name}")
            st.markdown("by **scStudio**")
            st.markdown("---")
            st.markdown('<div class="sidebar-button">Chat history</div>', unsafe_allow_html=True)
            st.markdown('<div class="sidebar-button">Make my own games</div>', unsafe_allow_html=True)
            st.markdown('<div class="sidebar-button">Code a AI</div>', unsafe_allow_html=True)
            st.markdown('<div class="sidebar-button">Roblox has ban</div>', unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("<p style='font-size: 14px;'>scStudio<br>Free mode</p>", unsafe_allow_html=True)

        col1, col2 = st.columns([1, 6])
        with col1:
            st.markdown("## ZEDA.AI")
        with col2:
            st.markdown("<p style='text-align: right; color: #888;'>zeda0.5</p>", unsafe_allow_html=True)

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
        # ใช้ config['preauthorized']['emails'] ในฟังก์ชัน register_user
        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(
            'Register user', 
            preauthorization=config['preauthorized']['emails']
        )
        if email_of_registered_user:
            st.success('User registered successfully!')
            
            with open('config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
            st.info("โปรดล็อกอินด้วยข้อมูลที่คุณเพิ่งลงทะเบียน")

    except Exception as e:
        st.error(e)


