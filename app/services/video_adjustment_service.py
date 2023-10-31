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

# Resize ant 1:1 video into 720x720
def rescale_to_720x720(file_path):
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
        remove_video_file(file_path)
        print(f"Video has been converted to 720x720 and saved as {file_path}")

        return new_file_path

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {str(e)}")
        return False
    
# Crop Resize any video to 720x720
def crop_and_resize_to_720x720(file_path):
    directory, filename = os.path.split(file_path)
    new_file_name = generate_random_name(10) + '.mp4'
    new_file_path = os.path.join(directory, new_file_name)

    try:
        # Get the video dimensions
        command = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height',
            '-of', 'csv=s=x:p=0',
            file_path
        ]
        video_info = subprocess.check_output(command).decode().strip().split('x')
        video_width, video_height = int(video_info[0]), int(video_info[1])

        # Calculate the cropping dimensions for right-middle cropping
        crop_width = min(video_width, video_height)
        crop_x = 0
        crop_y = int((video_height - crop_width)/2)

        # Use FFmpeg to crop and resize the video to 720x720 resolution with right-middle cropping
        command = [
            'ffmpeg',
            '-i', file_path,                             # Input video file
            '-vf', f'crop={crop_width}:{crop_width}:{crop_x}:{crop_y},scale=720:720',  # Crop from the right middle and then resize
            '-c:a', 'copy',                              # Copy audio codec
            '-y',                                        # Overwrite the input file
            new_file_path                                # Output video file with the same filename
        ]

        subprocess.run(command, check=True)
        remove_video_file(file_path)
        print(f"Video has been cropped and resized to 720x720 and saved as {new_file_path}")

        return new_file_path

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {str(e)}")
        remove_video_file(file_path)
        return False

