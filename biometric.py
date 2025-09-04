import face_recognition
import cv2

def encode_face(image):
    """Takes an OpenCV image and returns face encoding"""
    rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb_img)
    return encodings[0] if encodings else None

def verify_face(known_encoding, frame):
    """Compare stored encoding with a new frame"""
    rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb_img)
    if not encodings:
        return "no_face"
    result = face_recognition.compare_faces([known_encoding], encodings[0])[0]
    return "match" if result else "mismatch"
