# auth.py — Password & Biometric helpers
import bcrypt
import numpy as np
from PIL import Image
import io
import face_recognition
import streamlit as st

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

def capture_face_streamlit(label: str):
    img_file = st.camera_input(label)
    if img_file is None:
        return None
    bytes_data = img_file.getvalue()
    pil_img = Image.open(io.BytesIO(bytes_data)).convert("RGB")
    return np.array(pil_img)

def encode_face(rgb_image_ndarray: np.ndarray):
    encs = face_recognition.face_encodings(rgb_image_ndarray)
    if encs:
        return encs[0]
    return None

def verify_biometric(live_encoding: np.ndarray, stored_encoding_bytes: bytes) -> bool:
    stored = np.frombuffer(stored_encoding_bytes, dtype=np.float64)
    matches = face_recognition.compare_faces([stored], live_encoding)
    return bool(matches[0])
