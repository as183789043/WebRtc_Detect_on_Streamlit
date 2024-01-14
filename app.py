import streamlit  as st
import av
from streamlit_webrtc import webrtc_streamer
from turn import get_ice_servers

def webcam_input():
    st.header("Webcam Live Feed")
    WIDTH = st.sidebar.select_slider('QUALITY (May reduce the speed)', list(range(150, 501, 50)))
    width = WIDTH



    def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
        image = frame.to_ndarray(format="bgr24")

        orig_h, orig_w = image.shape[0:2]

        # cv2.resize used in a forked thread may cause memory leaks
        input = np.asarray(Image.fromarray(image).resize((width, int(width * orig_h / orig_w))))

        transferred = style_transfer(input, model)

        result = Image.fromarray((transferred * 255).astype(np.uint8))
        image = np.asarray(result.resize((orig_w, orig_h)))
        return av.VideoFrame.from_ndarray(image, format="bgr24")
    
    ctx = webrtc_streamer(
        key="neural-style-transfer",
        video_frame_callback=video_frame_callback,
        rtc_configuration={"iceServers": get_ice_servers()},
        media_stream_constraints={"video": True, "audio": False},
    )


st.sidebar.title("Get permission about Web Camera ")

webcam_input()