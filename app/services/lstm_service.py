import tensorflow as tf
import numpy as np

from app.dto.json_req_dto import JsonLandmark

class LSTM():
    def __init__(self, classes, highest_frame = 120, step_size = 1):
        self.classes = classes
        self.highest_frame = highest_frame
        self.step_size = step_size
        self.lstm_model = tf.keras.models.load_model('./app/ml_models/six_class_model_3_frame_steps')
        self.lstm_model.summary()

    # Add padding, limit number of frames and use steps to preprocess text landmarks
    def preprocess_text_landmarks(self, x, y):
        # Pad numpy arrays if they are short
        # Calculate the amount of padding needed
        padding_rows = max(0, self.highest_frame - x.shape[0])
        x = np.pad(x, ((0, padding_rows), (0, 0)), mode='constant', constant_values=0)
        y = np.pad(y, ((0, padding_rows), (0, 0)), mode='constant', constant_values=0)

        x = x[:self.highest_frame:self.step_size, :]
        y = y[:self.highest_frame:self.step_size, :]
            
        # reshape to eg (1, 40, 12)
        x = x.reshape((1, int(self.highest_frame/self.step_size), 12))
        y = y.reshape((1, int(self.highest_frame/self.step_size), 12))

        return x, y
    
    # Add padding, limit number of frames and use steps to preprocess video landmarks
    def preprocess_video_landmarks(self, x, y):
        # Pad numpy arrays if they are short
        # Calculate the amount of padding needed
        maximum_frames = int(self.highest_frame/self.step_size)
        padding_rows = max(0, maximum_frames - x.shape[0])
        x = np.pad(x, ((0, padding_rows), (0, 0)), mode='constant', constant_values=0)
        y = np.pad(y, ((0, padding_rows), (0, 0)), mode='constant', constant_values=0)

        x = x[:maximum_frames:, :]
        y = y[:maximum_frames:, :]

        # reshape to eg (1, 40, 12)
        x = x.reshape((1, maximum_frames, 12))
        y = y.reshape((1, maximum_frames, 12))

        return x, y

    
    def find_class(self, value):
        for key, val in self.classes.items():
            if val == value:
                return key
        return None 


    def predict(self, x, y):
        predicted_class = False

        try:
            predicted_probabilities = self.lstm_model.predict([x, y])

            # Convert probabilities to class labels by taking the argmax
            predicted_labels = np.argmax(predicted_probabilities, axis=1)
            predicted_class = self.find_class(predicted_labels[0])

            print(f"Successful prediction: {predicted_class}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            return predicted_class
        
    def json_to_numpy(self, obj: JsonLandmark):
        try:
            x = [[sublist[i] for i in range(0, len(sublist), 2)] for sublist in obj.landmarks]
            y = [[sublist[i] for i in range(1, len(sublist), 2)] for sublist in obj.landmarks]

            x = np.array(x)
            y = np.array(y)

            return x, y, False
        except Exception as e:
            print(f"Error: {e}")

            return None, None, True

