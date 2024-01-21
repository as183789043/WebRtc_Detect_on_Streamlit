
import cv2
import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer,WebRtcMode,RTCConfiguration
from ultralytics import YOLO
import av 

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

model=YOLO("yolov8n.pt")


def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")

    results = model(img)
    annotated_frame = results[0].plot()

    return av.VideoFrame.from_ndarray(annotated_frame, format="bgr24")


ctx = webrtc_streamer(key="example",      
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        video_frame_callback=video_frame_callback,
        async_processing=True,)

