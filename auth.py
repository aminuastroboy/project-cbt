import bcrypt
import numpy as np
from deepface import DeepFace
import streamlit as st
from PIL import Image
import io
import base64

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def encode_face(image_file):
    image = Image.open(io.BytesIO(image_file.getvalue()))
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def verify_face(image_file, stored_face_b64):
    if not stored_face_b64:
        return False
    try:
        stored_bytes = base64.b64decode(stored_face_b64)
        stored_image = Image.open(io.BytesIO(stored_bytes))
        live_image = Image.open(io.BytesIO(image_file.getvalue()))
        result = DeepFace.verify(np.array(live_image), np.array(stored_image), enforce_detection=False)
        return result.get("verified", False)
    except Exception as e:
        st.error(f"DeepFace error: {e}")
        return False
