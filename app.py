import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer,WebRtcMode
from ultralytics import YOLO
from pytubefix import YouTube
from PIL import Image
# other file
from helper import *
from turn import get_ice_servers
from streamlit_player import st_player

with st.sidebar:
    st.title("Object Detect Base on YOLO8")
    model_name=st.selectbox("推論模型",options=["yolov8n.pt"],index=0
    )

    option = st.radio(label="Detect Mode",
    options=["Image","Video","Webcam","RTSP","Youtube"])




if  option=="Image":
    Image=st.sidebar.file_uploader("上傳圖片進行物件辨識",type=['png', 'jpg'])
    buttom=st.sidebar.button("進行影像辨識")

    if buttom==1 and Image ==None:
        st.toast('要先上傳圖片才能辨識喔!')

    elif buttom and Image:
            st.image(Image,caption="原圖")
            st.image(image_process(Image,model_name),caption="辨識結果")


    elif Image :
        st.image(Image,caption="原圖檢查")



if  option=="Video":
    Video=st.sidebar.file_uploader("上傳影片進行物件辨識", type=["mp4", "mpeg"])
    buttom=st.sidebar.button("進行影片辨識")
    # Open the video file


    if buttom==1 and Video==None:
        st.toast('要先上傳影片才能辨識喔!')

    elif buttom and Video:
        st.subheader("原影片")
        st.video(Video)
        st.subheader("影片辨識結果")

        tfile =video_to_tempfile(Video)
        vf = cv2.VideoCapture(tfile.name)

        stframe = st.empty()
        while vf.isOpened():
            ret, frame = vf.read()
            # if frame is read correctly ret is True
            if not ret:
                vf.release()
                stframe.empty()
            else:
                annotated_frame = predict_every_frame(model_name,frame)
                stframe.image(annotated_frame)

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
                video_frame_callback=lambda frame: video_frame_callback(frame, model_name),
                media_stream_constraints={"video": True, "audio": False},
                async_processing=True,)


if option=="RTSP":
    RTSP_endpoint=st.sidebar.text_input("請輸入RTSP連線端點")
    st.sidebar.write("Example URL: rtsp://{username}:{passwoed}@{ip}:{port}/h264_ulaw.sdp") #support h264 video encoding
    if RTSP_endpoint:
        fourcc = cv2.VideoWriter_fourcc('H', '2', '6', '4')  

        vid_cap = cv2.VideoCapture(RTSP_endpoint)

        st_frame = st.empty()
        while (vid_cap.isOpened()):
            success, image = vid_cap.read()
            if success:
                annotated_frame=predict_every_frame(model_name,image)
                st_frame.image(annotated_frame)
            else:
                vid_cap.release()
                break
    else:
        st.toast('請輸入RTSP連線端點')



if option=='Youtube':
    url = st.sidebar.text_input("請輸入Youtube影片url")
    buttom=st.sidebar.button("進行影片辨識")
    if url and buttom :
        st.subheader("Youtube原始影片")
        st_player(url)

        st.subheader("Youtube影片辨識結果")
        yt = YouTube(url)
        stream = yt.streams.filter(res=720).first()
        vid_cap = cv2.VideoCapture(stream.url)

        st_frame = st.empty()
        while (vid_cap.isOpened()):
            success, image = vid_cap.read()
            if success:
                annotated_frame=predict_every_frame(model_name,image)
                st_frame.image(annotated_frame)
            else:
                vid_cap.release()
                break
    elif url:
        st.toast('點擊影像辨識按鈕開始分析!')
    else:
        st.toast('請輸入Youtube影片url')

