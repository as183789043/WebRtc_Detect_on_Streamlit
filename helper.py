import av
import streamlit as st
from ultralytics import YOLO
import numpy as np
from PIL import Image
#Model
@st.cache_resource
def load_model(model_name):
    return YOLO(model_name)

#Image type to numpy
def image_process(upload_image,model_name):
    img= Image.open(upload_image)
    np_img = np.array(img) #nparray
    model = load_model(model_name)
    results = model(np_img)
    for result in results:
        return result.plot()


#WebRTC Process
def video_frame_callback(frame,model_name):
    img = frame.to_ndarray(format="bgr24")
    model = load_model(model_name)
    results = model(img)
    annotated_frame = results[0].plot()

    return av.VideoFrame.from_ndarray(annotated_frame, format="bgr24")
