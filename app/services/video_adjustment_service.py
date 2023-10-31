import cv2
import os
import subprocess

from app.utils.utils import generate_random_name, remove_video_file

def check_video_resolution(filename):
    try:
        cap = cv2.VideoCapture(filename)
        if not cap.isOpened():
            return 2

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if width == int(os.getenv("VIDEO_WIDTH")) and height == int(os.getenv("VIDEO_HEIGHT")):
            return 0
        elif width == height:
            return 1
        else:
            return 2

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 3


def convert_to_720x720(file_path):
    directory, filename = os.path.split(file_path)
    new_file_name = generate_random_name(10) + '.mp4'

    new_file_path = os.path.join(directory, new_file_name)

    try:
        # Use FFmpeg to convert the video to 720x720 resolution and save it with the same filename
        command = [
            'ffmpeg',
            '-i', file_path,             # Input video file
            '-vf', 'scale=720:720',      # Set the resolution to 720x720
            '-c:a', 'copy',              # Copy audio codec
            '-y',                        # Overwrite the input file
            new_file_path                    # Output video file with the same filename
        ]

        subprocess.run(command, check=True)
        print(f"Video has been converted to 720x720 and saved as {file_path}")

        return new_file_path

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {str(e)}")
        return False

