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
        x = x[:self.max_frames:self.step_size, :]
        y = y[:self.max_frames:self.step_size, :]
        
        x = x.reshape((1, 40, 12))
        y = y.reshape((1, 40, 12))
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
        return self.find_class(predicted_labels[0])