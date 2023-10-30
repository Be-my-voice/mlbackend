import mediapipe as mp
import cv2
from mediapipe.framework.formats import landmark_pb2
import numpy as np
import os

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def extract_skeleton(filename):
    data_x = []
    data_y = []

    frame_number = 0

    cap = cv2.VideoCapture(filename)
    while cap.isOpened():
        x_data = []
        y_data = []


        ret, frame = cap.read()

        if not ret:
            break

        if(frame_number % int(os.getenv("STEP_SIZE")) != 0):
             frame_number += 1
             continue
        else:
             frame_number += 1

        try:
            rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgbFrame)
            finalRes = landmark_pb2.NormalizedLandmarkList(landmark = results.pose_landmarks.landmark[11:23])

            j = finalRes.landmark[0]

            for i in range(0,12):
                    j = finalRes.landmark[i]
                    x_data.append(j.x)
                    y_data.append(j.y)
        
        except Exception as e:
            print(f"Error: {e}")

        finally:
            data_x.append(x_data)
            data_y.append(y_data)

    
    # Convert the lists to NumPy arrays
    data_x = np.array(data_x)
    data_y = np.array(data_y)
    return data_x, data_y       