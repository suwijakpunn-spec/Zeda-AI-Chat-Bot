import streamlit as st
import google.generativeai as genai
import os
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# --- Set up the page and CSS ---
st.set_page_config(
    page_title="ZEDA.AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* Adjust font throughout the app */
body {
    font-family: sans-serif;
}

/* Adjust background colors of the main page and sidebar */
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

/* Hide unwanted Streamlit components */
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

/* Customize the sidebar */
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

/* Create custom buttons with HTML/CSS */
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

# --- AI and main code section ---
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# --- User Authentication ---
try:
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
except FileNotFoundError:
    st.error("Cannot find config.yaml. Please create the file with the recommended settings.")
    st.stop()

# Correctly initialize Authenticator for the new version
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# --- Login and Register options ---
st.sidebar.title("ZEDA.AI")
st.sidebar.markdown("by **scStudio**")
choice = st.sidebar.radio("Select Menu", ["Login", "Register"])

if choice == "Login":
    st.title("Login")
    # Correct login function call
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

        # Chat box
        if "messages" not in st.session_state:
            st.session_state.messages = []
            st.session_state.messages.append({"role": "assistant", "content": "Hello! I am Zeda AI, using a model from Google. How can I help you today?"})
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("type anythings..."):
            prompt_lower = prompt.lower()
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user"):
                st.markdown(prompt)

            if "your name" in prompt_lower or "What is your name" in prompt_lower:
                response_text = "My name is Zeda. I'm an AI developed by scStudio using a Google model."
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
                            st.error(f"An error occurred: {e}")

    elif authentication_status == False:
        st.error('Username/password is incorrect')
    elif authentication_status == None:
        st.warning('Please enter your username and password')

elif choice == "Register":
    st.title("Register New User")
    try:
        # The 'preauthorization' parameter is now part of the register_user function, not Authenticate
        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(
            'Register user',
            preauthorization=False
        )
        if email_of_registered_user:
            st.success('User registered successfully!')
            
            with open('config.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
            st.info("Please log in with your newly registered information.")

    except Exception as e:
        st.error(e)
