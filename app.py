import streamlit as st
import json
from biometric import capture_and_register, capture_and_verify

DB_FILE = "db.json"

def load_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": {}, "results": {}}

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f)

db = load_db()

st.title("🖥️ CBT with Biometric Verification")

menu = ["Register", "Login & Exam", "Check Results"]
choice = st.sidebar.radio("Menu", menu)

if choice == "Register":
    st.header("Register User")
    email = st.text_input("Email")
    name = st.text_input("Full Name")
    if st.button("Capture Face and Register"):
        face_encoding = capture_and_register()
        if face_encoding:
            db["users"][email] = {"name": name, "face_encoding": face_encoding}
            save_db(db)
            st.success("✅ Registered successfully!")

elif choice == "Login & Exam":
    st.header("Login with Face Verification")
    email = st.text_input("Enter Email")
    if st.button("Verify and Start Exam"):
        if email in db["users"]:
            result = capture_and_verify(db["users"][email]["face_encoding"])
            if result == "match":
                st.success("✅ Identity verified! Starting exam...")
                q1 = st.radio("Q1: 2 + 2 = ?", ["3", "4", "5"])
                if st.button("Submit Exam"):
                    score = 1 if q1 == "4" else 0
                    db["results"][email] = {"score": score}
                    save_db(db)
                    st.success(f"Exam submitted! Your score: {score}")
            else:
                st.error("❌ Face not matched.")
        else:
            st.error("⚠️ User not found. Please register.")

elif choice == "Check Results":
    st.header("Check Results with Face Verification")
    email = st.text_input("Enter Email")
    if st.button("Verify and Show Result"):
        if email in db["users"] and email in db["results"]:
            result = capture_and_verify(db["users"][email]["face_encoding"])
            if result == "match":
                st.success(f"✅ Your score: {db['results'][email]['score']}")
            else:
                st.error("❌ Verification failed.")
        else:
            st.error("⚠️ No exam results found.")
