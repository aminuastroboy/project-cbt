import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av
import json
import cv2
import numpy as np
from biometric import encode_face, verify_face

# ---- Storage (use DB later) ----
DB_FILE = "db.json"
try:
    with open(DB_FILE, "r") as f:
        db = json.load(f)
except:
    db = {"users": {}, "results": {}}

def save_db():
    with open(DB_FILE, "w") as f:
        json.dump(db, f)

# ---- WebRTC Transformer ----
class FaceCapture(VideoTransformerBase):
    def __init__(self):
        self.frame = None
    def transform(self, frame):
        self.frame = frame.to_ndarray(format="bgr24")
        return self.frame

# ---- Pages ----
def register():
    st.subheader("📝 Register")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    name = st.text_input("Full Name")

    ctx = webrtc_streamer(key="register", video_transformer_factory=FaceCapture)

    if st.button("Register"):
        if ctx.video_transformer and ctx.video_transformer.frame is not None:
            encoding = encode_face(ctx.video_transformer.frame)
            if encoding is not None:
                db["users"][email] = {"password": password, "encoding": encoding.tolist(), "name": name}
                db["results"][email] = {"score": 75}  # dummy score
                save_db()
                st.success("✅ Registered successfully with biometric data!")
            else:
                st.error("⚠️ No face detected. Try again.")
        else:
            st.error("⚠️ Camera not active.")

def login():
    st.subheader("🔑 Login to Exam")
    email = st.text_input("Email (login)")
    password = st.text_input("Password (login)", type="password")

    ctx = webrtc_streamer(key="login", video_transformer_factory=FaceCapture)

    if st.button("Login"):
        if email in db["users"] and db["users"][email]["password"] == password:
            known_encoding = np.array(db["users"][email]["encoding"])
            if ctx.video_transformer and ctx.video_transformer.frame is not None:
                result = verify_face(known_encoding, ctx.video_transformer.frame)
                if result == "match":
                    st.success("✅ Biometric Verified! Access granted to exam.")
                elif result == "mismatch":
                    st.error("❌ Face mismatch! Access denied.")
                else:
                    st.warning("⚠️ No face detected.")
            else:
                st.error("⚠️ Camera not active.")
        else:
            st.error("❌ Invalid credentials.")

def check_results():
    st.subheader("📊 Check Results")
    email = st.text_input("Email")
    ctx = webrtc_streamer(key="results", video_transformer_factory=FaceCapture)

    if st.button("Verify & Show Results"):
        if email in db["users"]:
            known_encoding = np.array(db["users"][email]["encoding"])
            if ctx.video_transformer and ctx.video_transformer.frame is not None:
                result = verify_face(known_encoding, ctx.video_transformer.frame)
                if result == "match":
                    st.success(f"✅ Verified! Your score: {db['results'][email]['score']}%")
                elif result == "mismatch":
                    st.error("❌ Face mismatch! Cannot show results.")
                else:
                    st.warning("⚠️ No face detected.")
            else:
                st.error("⚠️ Camera not active.")
        else:
            st.error("❌ No such user found.")

# ---- Main ----
st.title("📚 CBT with Biometric Verification")

page = st.sidebar.selectbox("Navigate", ["Register", "Login (Exam)", "Check Results"])
if page == "Register":
    register()
elif page == "Login (Exam)":
    login()
elif page == "Check Results":
    check_results()
