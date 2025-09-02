import streamlit as st
import google.generativeai as genai
import os
import streamlit_authenticator as stauth
import yaml
import sqlite3

# --- การตั้งค่าทั่วไปของหน้าเว็บ ---
st.set_page_config(
    page_title="ZEDA.AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- โค้ด CSS สำหรับปรับแต่งหน้าตา ---
st.markdown("""
<style>
/* ... โค้ด CSS ที่คุณมีอยู่แล้ว ... */
</style>
""", unsafe_allow_html=True)

# --- การสร้างและเชื่อมต่อฐานข้อมูล ---
conn = sqlite3.connect('chat_history.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS chats
             (username TEXT, role TEXT, content TEXT)''')

# --- การทำระบบ Login ---
with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # --- ส่วนของโค้ด AI และการทำงานหลัก ---
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash")

    # Sidebar
    with st.sidebar:
        authenticator.logout('Logout', 'main')
        st.image("https://i.ibb.co/L50HjHj/ZEDA-AI.png", width=150)
        st.markdown("## zeda0.5")
        st.markdown(f"by **scStudio**")
        st.markdown("---")
        st.markdown('<div class="sidebar-button">Chat history</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-button">Make my own games</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-button">Code a AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-button">Roblox has ban</div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(f"**Logged in as:** {username}")
        st.markdown("<p style='font-size: 14px;'>scStudio<br>Free mode</p>", unsafe_allow_html=True)

    # Main content
    col1, col2 = st.columns([1, 6])
    with col1:
        st.markdown("## ZEDA.AI")
    with col2:
        st.markdown("<p style='text-align: right; color: #888;'>zeda0.5</p>", unsafe_allow_html=True)

    # สร้างกล่องแชทและโหลดประวัติการแชทจาก DB
    if "messages" not in st.session_state:
        st.session_state.messages = []
        c.execute("SELECT role, content FROM chats WHERE username = ?", (username,))
        history = c.fetchall()
        for role, content in history:
            st.session_state.messages.append({"role": role, "content": content})
        
        if not st.session_state.messages:
             st.session_state.messages.append({"role": "assistant", "content": "สวัสดีครับ ผมคือ Zeda AI ที่ใช้โมเดลจาก Google มีอะไรให้ผมช่วยไหมครับ?"})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("type anythings..."):
        prompt_lower = prompt.lower()
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # บันทึกข้อความของผู้ใช้ลงในฐานข้อมูล
        c.execute("INSERT INTO chats VALUES (?, ?, ?)", (username, "user", prompt))
        conn.commit()

        if "your name" in prompt_lower or "ชื่ออะไร" in prompt_lower or "คุณชื่ออะไร" in prompt_lower:
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
                        
                        # บันทึกข้อความของ AI ลงในฐานข้อมูล
                        c.execute("INSERT INTO chats VALUES (?, ?, ?)", (username, "assistant", response.text))
                        conn.commit()
                    except Exception as e:
                        st.error(f"เกิดข้อผิดพลาด: {e}")
    conn.close()
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
