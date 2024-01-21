def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    model = load_model()
    results = model(img)
    annotated_frame = results[0].plot()

    return av.VideoFrame.from_ndarray(annotated_frame, format="bgr24")
