import av
import streamlit as st
from ultralytics import YOLO
import numpy as np
from PIL import Image
import tempfile  #暫存用戶上傳video file
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
    
# predict every frame
def predict_every_frame(model_name,frame):
    model = load_model(model_name)
    results = model(frame)
    annotated_frame = results[0].plot()
    return annotated_frame


#WebRTC Process
def video_frame_callback(frame,model_name):
    img = frame.to_ndarray(format="bgr24")
    predict_every_frame()

    return av.VideoFrame.from_ndarray(annotated_frame, format="bgr24")


# Upload video to temfile
def video_to_tempfile(video):
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(video.read())
    return tfile



