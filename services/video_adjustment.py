import cv2
import os

def check_video_resolution(filename):
    try:
        cap = cv2.VideoCapture(filename)
        if not cap.isOpened():
            return 2

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if width == int(os.getenv("VIDEO_WIDTH")) and height == int(os.getenv("VIDEO_HEIGHT")):
            return 0
        else:
            return 1

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 2
