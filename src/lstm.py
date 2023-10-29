import tensorflow as tf
import numpy as np

class LSTM():
    def __init__(self, classes, max_frames = 120, step_size = 1):
        self.classes = classes
        self.max_frames = max_frames
        self.step_size = step_size
        self.lstm_model = tf.keras.models.load_model('./ml_models/six_class_model_3_frame_steps')
        self.lstm_model.summary()

    
    def preprocess(self, x, y):
        # Pad numpy arrays if they are short
        # Calculate the amount of padding needed
        try:
            padding_rows = max(0, self.max_frames - x.shape[0])
            x = np.pad(x, ((0, padding_rows), (0, 0)), mode='constant', constant_values=0)
            y = np.pad(y, ((0, padding_rows), (0, 0)), mode='constant', constant_values=0)

            x = x[:self.max_frames:self.step_size, :]
            y = y[:self.max_frames:self.step_size, :]
            
            # reshape to eg (1, 40, 12)
            x = x.reshape((1, int(self.max_frames/self.step_size), 12))
            y = y.reshape((1, int(self.max_frames/self.step_size), 12))
            return x, y
        except Exception as e:
            print(f"Error: {e}")
            return x, y
    
    
    def find_class(self, value):
        for key, val in self.classes.items():
            if val == value:
                return key
        return None 


    def predict(self, x, y):
        x, y = self.preprocess(x, y)

        predicted_probabilities = self.lstm_model.predict([x, y])

        # Convert probabilities to class labels by taking the argmax
        predicted_labels = np.argmax(predicted_probabilities, axis=1)
        predicted_class = self.find_class(predicted_labels[0])

        print(f"Successful prediction: {predicted_class}")
        return predicted_class