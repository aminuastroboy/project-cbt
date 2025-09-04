import streamlit as st
import face_recognition
from PIL import Image

# ---------------------------
# Helper functions
# ---------------------------
def encode_face(uploaded_file):
    """Convert uploaded image to face encoding vector."""
    if uploaded_file is None:
        return None
    image = face_recognition.load_image_file(uploaded_file)
    encodings = face_recognition.face_encodings(image)
    return encodings[0] if encodings else None

def verify_face(known_encoding, uploaded_file):
    """Compare new face with stored encoding."""
    if uploaded_file is None or known_encoding is None:
        return False
    image = face_recognition.load_image_file(uploaded_file)
    encodings = face_recognition.face_encodings(image)
    if not encodings:
        return False
    return face_recognition.compare_faces([known_encoding], encodings[0])[0]

# ---------------------------
# Session state setup
# ---------------------------
if "user" not in st.session_state:
    st.session_state["user"] = None
if "users" not in st.session_state:
    st.session_state["users"] = []
if "exams" not in st.session_state:
    st.session_state["exams"] = []

st.set_page_config(page_title="CBT with Biometrics", layout="wide")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------------------
# REGISTER
# ---------------------------
if choice == "Register":
    st.subheader("📝 Register")
    first = st.text_input("First Name")
    last = st.text_input("Last Name")
    email = st.text_input("Email")
    role = st.selectbox("Role", ["student", "admin", "invigilator"])
    password = st.text_input("Password", type="password")
    face_file = st.file_uploader("Upload Face Image (for biometric login)", type=["jpg","jpeg","png"])

    if st.button("Register"):
        face_encoding = encode_face(face_file)
        if face_encoding is None:
            st.error("❌ No face detected. Please try again.")
        else:
            st.session_state["users"].append({
                "first_name": first,
                "last_name": last,
                "email": email,
                "password": password,
                "role": role,
                "biometric": face_encoding
            })
            st.success("✅ User registered with biometric data")

# ---------------------------
# LOGIN
# ---------------------------
elif choice == "Login":
    st.subheader("🔑 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    face_file = st.file_uploader("Upload Face Image for Verification", type=["jpg","jpeg","png"])

    if st.button("Login"):
        user = next((u for u in st.session_state["users"] if u["email"] == email and u["password"] == password), None)
        if user:
            if verify_face(user["biometric"], face_file):
                st.session_state["user"] = user
                st.success(f"✅ Biometric verified! Welcome {user['first_name']} ({user['role']})")
            else:
                st.error("❌ Face mismatch. Access denied.")
        else:
            st.error("Invalid credentials")

# ---------------------------
# DASHBOARDS
# ---------------------------
if st.session_state["user"]:
    role = st.session_state["user"]["role"]

    if role == "admin":
        st.header("⚙️ Admin Dashboard")
        st.info("Admin can create exams and manage questions.")
    elif role == "student":
        st.header("🎓 Student Dashboard")
        st.info("Student can take exams.")
    elif role == "invigilator":
        st.header("🕵️ Invigilator Dashboard")
        st.info("Invigilator can monitor exams.")
