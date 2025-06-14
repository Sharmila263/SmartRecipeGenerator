import streamlit as st
from auth import register_user, login_user
import os
import base64
import time

st.set_page_config(page_title="Smart Recipe Generator", layout="centered")
from db import create_database

# Ensure DB is created when app runs
create_database()

# Set background image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{b64}");
            background-size: cover;
            background-position: center;
        }}
        </style>
    """, unsafe_allow_html=True)

add_bg_from_local("assets/bg.jpg")

# Custom CSS: Fonts, Colors, Input Boxes, Buttons
st.markdown("""
    <style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Pacifico&family=Dancing+Script&display=swap');

    .stApp {
        color: white !important;
    }

    /* Beautiful title font */
    .main-title {
        font-family: 'Pacifico', cursive;
        font-size: 3em;
        color: white;
        margin-bottom: 0;
    }

    .sub-title {
        font-family: 'Dancing Script', cursive;
        font-size: 1.5em;
        color: #f8f8f8;
        margin-top: 0;
        margin-bottom: 20px;
    }

    .page-heading {
        font-family: 'Dancing Script', cursive;
        font-size: 2em;
        font-weight: bold;
        margin-top: 30px;
        color: white;
    }

    .form-container {
        background-color: rgba(0, 0, 0, 0.65);
        padding: 30px;
        border-radius: 12px;
        max-width: 500px;
        margin: auto;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
    }

    label, .css-1cpxqw2 {
        color: white !important;
        font-weight: 500;
    }

    .stTextInput > div > div > input,
    .stTextArea > div > textarea,
    .stSelectbox > div,
    .stTextInput input {
        background-color: #1e1e1e;
        color: white;
        border: 1px solid #888;
        border-radius: 8px;
    }

    .stButton > button {
        background-color: #a83279;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        transition: background-color 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #6a1b4d;
    }

    h1, h2, h3 {
        color: white;
    }
    /* Fix tab label visibility */
.stTabs [data-baseweb="tab"] {
    color: white !important;
    font-weight: bold;
    font-size: 16px;
}

.stTabs [aria-selected="true"] {
    border-bottom: 3px solid #a83279 !important;
    color: #ffdef2 !important;
    background-color: rgba(255, 255, 255, 0.05);
}

    </style>
""", unsafe_allow_html=True)

# Title and subtitle
st.markdown("""
<div style='text-align: center; padding: 20px 0;'>
    <div class='main-title'>🍳 Snap & Savor</div>
    <div class='sub-title'>Your AI-Powered Smart Recipe Generator</div>
</div>
""", unsafe_allow_html=True)


# Initialize session state
if "user" not in st.session_state:
    st.session_state.user = None

# Tabs for login/register
tab1, tab2 = st.tabs(["Login", "Register"])

# Register Tab
with tab2:
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.subheader("Register")

    name = st.text_input("New Username", key="reg_name")
    password = st.text_input("New Password", type="password", key="reg_pass")
    phone = st.text_input("Phone Number", key="reg_phone")
    email = st.text_input("Email ID", key="reg_email")
    profile_pic = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"], key="reg_pic")

    if st.button("Register"):
        if all([name.strip(), password.strip(), email.strip()]):  
            pic_path = None
            if profile_pic:
                pic_path = os.path.join("assets", profile_pic.name)
                with open(pic_path, "wb") as f:
                    f.write(profile_pic.read())
            ok, msg = register_user(name, email, password, phone, pic_path)
            if ok:
                st.success(msg)
            else:
                st.error(msg)
        else:
            st.error("Please fill all mandatory fields (Name, Email, Password).")
    st.markdown('</div>', unsafe_allow_html=True)

# Login Tab
with tab1:
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.subheader("Login")

    email = st.text_input("Email", key="log_email")
    password = st.text_input("Password", type="password", key="log_pass")

    if st.button("Login"):
        success, user = login_user(email, password)
        if success:
            st.session_state.user = user
            st.success("Login successful! Redirecting...")
            time.sleep(1)
            st.switch_page("pages/Smart_Recipe_Generator.py")  # filename inside /pages (no .py)
        else:
            st.error("Invalid credentials")
    st.markdown('</div>', unsafe_allow_html=True)
