import bcrypt
import numpy as np
import streamlit as st
from PIL import Image

try:
    from deepface import DeepFace
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
    """Convert uploaded/camera image into face embedding."""
    if not DEEPFACE_AVAILABLE:
        return None
    try:
        # Convert UploadedFile (from st.camera_input) to numpy image
        image = Image.open(file)
        img_array = np.array(image)

        embedding = DeepFace.represent(
            img_path=img_array,
            model_name="VGG-Face",
            enforce_detection=False
        )[0]["embedding"]

        return np.array(embedding, dtype=np.float64).tobytes()
    except Exception as e:
        st.error(f"Face encoding failed: {e}")
        return None

def verify_face(file, stored_embedding):
    """Compare uploaded/camera image with stored embedding."""
    if not DEEPFACE_AVAILABLE:
        return False
    try:
        # Convert UploadedFile (from st.camera_input) to numpy image
        image = Image.open(file)
        img_array = np.array(image)

        embedding = DeepFace.represent(
            img_path=img_array,
            model_name="VGG-Face",
            enforce_detection=False
        )[0]["embedding"]

        return np.linalg.norm(
            np.array(embedding) - np.frombuffer(stored_embedding, dtype=np.float64)
        ) < 0.6
    except Exception as e:
        st.error(f"Face verification failed: {e}")
        return False
        
