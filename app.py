
import cv2
import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer,WebRtcMode,RTCConfiguration
from ultralytics import YOLO
from turn import get_ice_servers
from pytube import YouTube

with st.sidebar:
    st.title("Object Detect Base on YOLO8")
    st.selectbox("推論模型",options=["yolov8n.pt"],index=0
    )

    option = st.radio(label="Detect Mode",
    options=["Image","Video","Webcam","RTSP","Youtube"])


@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")

model=load_model()

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    results = model(img)
    annotated_frame = results[0].plot()

    return av.VideoFrame.from_ndarray(annotated_frame, format="bgr24")


if  option=="Image":
    Image=st.sidebar.file_uploader("上傳圖片進行物件辨識",type=['png', 'jpg'])
    buttom=st.sidebar.button("進行影像辨識")

    if buttom==1 and Image ==None:
        st.toast('要先上傳圖片才能辨識喔!')

    elif buttom and Image:
        col1, col2, = st.columns(2)
        with col1:
            st.image(Image.getvalue(),caption="原圖")

        with col2:
            st.image(Image.getvalue(),caption="未進行辨識(佔位)")


    elif Image :
        st.image(Image.getvalue(),caption="原圖檢查")



if  option=="Video":
    Video=st.sidebar.file_uploader("上傳影片進行物件辨識", type=["mp4", "mpeg"])
    buttom=st.sidebar.button("進行影片辨識")
    
    if buttom==1 and Video==None:
        st.toast('要先上傳影片才能辨識喔!')

    elif buttom and Video:
        st.subheader("原影片")
        st.video(Video)
        st.subheader("未辨識(佔位)")
        st.video(Video)

    elif Video:
        st.subheader("原影片")
        st.video(Video)

if option=="Webcam":
    warning = st.sidebar.warning("串流辨識因網速不同而有差異")
    check = st.sidebar.checkbox("瞭解上述提醒")

    if check ==1:
        ctx = webrtc_streamer(key="example",      
                mode=WebRtcMode.SENDRECV,
                rtc_configuration={"iceServers": get_ice_servers()},
                media_stream_constraints={"video": True, "audio": False},
                video_frame_callback=video_frame_callback,
                async_processing=True,)


if option=="RTSP":
    st.sidebar.text_input("請輸入RTSP連線端點")
    st.sidebar.write("Example URL: rtsp://admin:12345@192.168.1.210:554/Streaming/Channels/101")


if  option=="Youtube":
    url=st.sidebar.text_input("請輸入Youtube影片url")
    if url:
        yt = YouTube(url)
        stream = yt.streams.filter(file_extension="mp4", res=1080).get_highest_resolution()
        # vid_cap = cv2.VideoCapture(stream.url)
        st.subheader(f"{yt.title}")
        st.video(stream.url)
