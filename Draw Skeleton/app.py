import streamlit as st
import av
import cv2
import numpy as np
from streamlit_webrtc import (
    VideoProcessorBase,
    webrtc_streamer,
)
from loguru import logger

import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(static_image_mode=True, model_complexity=2, min_detection_confidence=0.5)

class myVidProcessor(VideoProcessorBase):

    def recv(self, frame):

        # frame is not of numpy array type, hence converting it.
        frm = frame.to_ndarray(format="bgr24")

        # getting the pose from mediapipe
        results = pose.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

        if results.pose_landmarks:
            # Draw pose landmarks on the image and save this image.
            mp_drawing.draw_landmarks(
                frm,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                )
        else :
            logger.warning("Failed to find pose for image")

        # DRAWING text message on the image
        cv2.rectangle(frm, (190, 380), (420, 480), (0, 0, 0), cv2.FILLED)
        cv2.putText(frm, "Sample text", (200, 455), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

        # expects av.VideoFrame or av.AudioFRame as return
        return av.VideoFrame.from_ndarray(frm, format = "bgr24")



st.title('Skeleton Drawing App')

st.sidebar.title('Controls')
# st.sidebar.subheader('sidebar subheader')

appmode = st.sidebar.selectbox("Type", ["Body pose", "Face mesh"])

if appmode == "Body pose":
    st.markdown('In this application we are using Mediapipe')

    # adding a divider in sidebar.
    st.sidebar.markdown("---")

    # Webrtc streamer for capturing webcam video, and showing the processed video.
    webrtc_streamer(
        key="pose-classifier",
        media_stream_constraints={"video": True, "audio": False},
        video_processor_factory=myVidProcessor
    )

    # Note : the recv method of the video_processor class is used for processing the video.

else:
    st.markdown("This page is under construction... Stay tuned !")
