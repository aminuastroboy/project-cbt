import sys, os
sys.path.append(os.path.dirname(__file__))

import streamlit as st
from db import init_db, get_conn
from auth import hash_password, verify_password, encode_face, verify_face

def safe_init_db():
    try:
        init_db()
        return True
    except Exception as e:
        st.warning(f"⚠️ Database connection failed: {e}")
        return False

st.title("📝 CBT System with Face Recognition")

db_ready = safe_init_db()

menu = ["Register", "Login"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register":
    st.subheader("Create New Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    face_image = st.camera_input("Take a picture for registration")

    if st.button("Register"):
        if not db_ready:
            st.error("Database not available. Please try again later.")
        elif username and password:
            try:
                conn = get_conn()
                cur = conn.cursor()
                query = "SELECT * FROM users WHERE username=%s" if hasattr(cur, "mogrify") else "SELECT * FROM users WHERE username=?"
                cur.execute(query, (username,))
                if cur.fetchone():
                    st.error("Username already exists.")
                else:
                    pw_hash = hash_password(password)
                    embedding = None
                    if face_image:
                        embedding = encode_face(face_image)
                    query = "INSERT INTO users (username, password_hash, face_embedding) VALUES (%s, %s, %s)" if hasattr(cur, "mogrify") else "INSERT INTO users (username, password_hash, face_embedding) VALUES (?, ?, ?)"
                    cur.execute(query, (username, pw_hash, embedding))
                    conn.commit()
                    st.success("Account created successfully!")
                cur.close()
                conn.close()
            except Exception as e:
                st.error(f"Error during registration: {e}")
        else:
            st.warning("Please fill in all fields.")

elif choice == "Login":
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    face_image = st.camera_input("Take a picture to verify your face")

    if st.button("Login"):
        if not db_ready:
            st.error("Database not available. Please try again later.")
        else:
            try:
                conn = get_conn()
                cur = conn.cursor()
                query = "SELECT password_hash, face_embedding FROM users WHERE username=%s" if hasattr(cur, "mogrify") else "SELECT password_hash, face_embedding FROM users WHERE username=?"
                cur.execute(query, (username,))
                user = cur.fetchone()
                cur.close()
                conn.close()

                if user:
                    pw_hash, stored_embedding = user[0], user[1]
                    if verify_password(password, pw_hash):
                        if stored_embedding and face_image:
                            if verify_face(face_image, stored_embedding):
                                st.success("Login successful with face recognition!")
                            else:
                                st.error("Face does not match.")
                        else:
                            st.success("Login successful (no face check).")
                    else:
                        st.error("Invalid password.")
                else:
                    st.error("User not found.")
            except Exception as e:
                st.error(f"Error during login: {e}")
