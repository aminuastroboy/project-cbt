import streamlit as st
import face_recognition
import numpy as np
import av
import cv2
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

class VideoTransformer(VideoTransformerBase):
    def __init__(self):
        self.frame = None

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        self.frame = img
        return img

def capture_and_register():
    st.write("📸 Align your face and click capture")
    ctx = webrtc_streamer(key="register", video_transformer_factory=VideoTransformer)
    
    if ctx.video_transformer and ctx.video_transformer.frame is not None:
        if st.button("Capture Face for Registration"):
            img = ctx.video_transformer.frame
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb_img)
            if encodings:
                return encodings[0].tolist()
            else:
                st.error("⚠️ No face detected, please try again.")
    return None

def capture_and_verify(stored_encoding):
    st.write("📸 Align your face and click verify")
    ctx = webrtc_streamer(key="verify", video_transformer_factory=VideoTransformer)

    if ctx.video_transformer and ctx.video_transformer.frame is not None:
        if st.button("Verify Face"):
            img = ctx.video_transformer.frame
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb_img)
            if encodings:
                match = face_recognition.compare_faces([np.array(stored_encoding)], encodings[0])[0]
                return "match" if match else "mismatch"
            else:
                return "no_face"
    return "no_input"
