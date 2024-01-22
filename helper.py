import av
import streamlit as st
from ultralytics import YOLO

@st.cache_resource
def load_model(model_name):
    return YOLO(model_name)


def video_frame_callback(frame,model_name):
    img = frame.to_ndarray(format="bgr24")
    model = load_model(model_name)
    results = model(img)
    annotated_frame = results[0].plot()

    return av.VideoFrame.from_ndarray(annotated_frame, format="bgr24")
