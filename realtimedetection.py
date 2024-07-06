import numpy as np
import cv2
from tensorflow.python.keras.models import model_from_json

class VideoCamera(object):
    def __init__(self):
        self.model = self.load_model()
        self.label = ['A', 'B', 'C', 'CALL ME', 'D', 'E', 'GOOD LUCK', 'HI', 'I LOVE U', 'PEACE', 'blank']
        self.cap = cv2.VideoCapture(0)

    def load_model(self):
        with open("signifymodel48x48.json", "r") as json_file:
            model_json = json_file.read()
        model = model_from_json(model_json)
        model.load_weights("signifymodel48x48.h5")
        return model

    def extract_features(self, image):
        feature = np.array(image)
        feature = feature.reshape(1, 48, 48, 1)
        return feature / 255.0

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, {"label": "No frame", "accuracy": "0"}

        # Draw ROI rectangle
        cv2.rectangle(frame, (0, 40), (300, 300), (0, 165, 255), 1)
        
        # Add instruction text above the ROI
        cv2.putText(frame, "Place your hand here", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2, cv2.LINE_AA)
        
        cropframe = frame[40:300, 0:300]
        cropframe = cv2.cvtColor(cropframe, cv2.COLOR_BGR2GRAY)
        cropframe = cv2.resize(cropframe, (48, 48))
        cropframe = self.extract_features(cropframe)
        pred = self.model.predict(cropframe)
        prediction_label = self.label[pred.argmax()]
        accu = "{:.2f}".format(np.max(pred) * 100)

        # Encode frame to JPEG format
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes(), {"label": prediction_label, "accuracy": accu}
