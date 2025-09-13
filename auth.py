import bcrypt
import numpy as np
import streamlit as st

try:
    from deepface import DeepFace
    from deepface.commons import functions
    import cv2
    DEEPFACE_AVAILABLE = True
except ImportError:
    DEEPFACE_AVAILABLE = False
    st.warning("⚠️ DeepFace is not available. Face recognition disabled.")

# -------------------
# Password utilities
# -------------------
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

# -------------------
# Face utilities
# -------------------
def encode_face(file):
    if not DEEPFACE_AVAILABLE:
        return None
    try:
        img = functions.preprocess_face(img=file, target_size=(224, 224), detector_backend="opencv")
        embedding = DeepFace.represent(img_path=img, model_name="VGG-Face", enforce_detection=False)[0]["embedding"]
        return np.array(embedding).tobytes()
    except Exception as e:
        st.error(f"Face encoding failed: {e}")
        return None

def verify_face(file, stored_embedding):
    if not DEEPFACE_AVAILABLE:
        return False
    try:
        img = functions.preprocess_face(img=file, target_size=(224, 224), detector_backend="opencv")
        embedding = DeepFace.represent(img_path=img, model_name="VGG-Face", enforce_detection=False)[0]["embedding"]
        return np.linalg.norm(np.array(embedding) - np.frombuffer(stored_embedding, dtype=np.float64)) < 0.6
    except Exception as e:
        st.error(f"Face verification failed: {e}")
        return False
