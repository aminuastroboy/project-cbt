import bcrypt
import numpy as np
import face_recognition
import streamlit as st
from PIL import Image
import io

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def encode_face(image_file):
    image = Image.open(io.BytesIO(image_file.getvalue()))
    img_array = np.array(image)
    encodings = face_recognition.face_encodings(img_array)
    return encodings[0].tobytes() if encodings else None

def verify_face(image_file, stored_encoding):
    if not stored_encoding:
        return False
    image = Image.open(io.BytesIO(image_file.getvalue()))
    img_array = np.array(image)
    encodings = face_recognition.face_encodings(img_array)
    if encodings:
        return face_recognition.compare_faces([np.frombuffer(stored_encoding, dtype=np.float64)], encodings[0])[0]
    return False
