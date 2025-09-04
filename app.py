# Streamlit main app
import streamlit as st
from db import init_db, get_exams, get_questions, create_exam, add_question, save_result
from auth import register_user, login_user

# Initialize DB
init_db()

st.set_page_config(page_title="CBT with Biometrics", layout="wide")

if 'user' not in st.session_state:
    st.session_state['user'] = None

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Login":
    st.subheader("🔑 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.session_state['user'] = user
            st.success(f"Welcome {user['first_name']} ({user['role']})")
        else:
            st.error("Invalid credentials")
elif choice == "Register":
    st.subheader("📝 Register")
    first = st.text_input("First Name")
    last = st.text_input("Last Name")
    email = st.text_input("Email")
    role = st.selectbox("Role", ["student", "admin", "invigilator"])
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if register_user(first, last, email, password, role):
            st.success("User registered ✅")
        else:
            st.error("Error registering user")

if st.session_state['user']:
    role = st.session_state['user']['role']
    if role == "admin":
        st.header("⚙️ Admin Dashboard")
        # Admin functionality
    elif role == "student":
        st.header("🎓 Student Dashboard")
        # Student functionality
    elif role == "invigilator":
        st.header("🕵️ Invigilator Dashboard")
        # Invigilator functionality
