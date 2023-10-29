import base64
import random
import string
import os

def base64ToVideo(filedata):

    file_name = "./temp/videos/{}.mp4".format(generate_random_name(10))

    image_as_bytes = str.encode(filedata)  # convert string to bytes
    img_recovered = base64.b64decode(image_as_bytes)  # decode base64string
    try:
        with open(file_name, "wb") as f:
            f.write(img_recovered)
            return file_name
    except Exception as e:
        print(f"Error: {e}")
        return False


def generate_random_name(length):
    characters = string.ascii_letters  # includes uppercase and lowercase letters
    random_name = ''.join(random.choice(characters) for _ in range(length))
    return random_name


def remove_video_file(filename):
    try:
        os.remove(filename)
    except OSError as e:
        print(f"Error: {e}")
