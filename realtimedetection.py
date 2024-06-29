import cv2
import numpy as np
from tensorflow.python.keras.models import model_from_json
class VideoCamera(object):
    def __init__(self):
        self.model = self.load_model()
        self.label = ['A', 'B', 'C', 'CALL ME', 'D', 'E', 'GOOD LUCK', 'HI', 'I LOVE U', 'PEACE', 'blank']
        self.cap = cv2.VideoCapture(0)

    def load_model(self):
        with open("signlanguagedetectionmodel48x48.json", "r") as json_file:
            model_json = json_file.read()
        model = model_from_json(model_json)
        model.load_weights("signlanguagedetectionmodel48x48.h5")
        return model

    def extract_features(self, image):
        feature = np.array(image)
        feature = feature.reshape(1, 48, 48, 1)
        return feature / 255.0

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None

        cv2.rectangle(frame, (0, 40), (300, 300), (0, 165, 255), 1)
        cropframe = frame[40:300, 0:300]
        cropframe = cv2.cvtColor(cropframe, cv2.COLOR_BGR2GRAY)
        cropframe = cv2.resize(cropframe, (48, 48))
        cropframe = self.extract_features(cropframe)
        pred = self.model.predict(cropframe)
        prediction_label = self.label[pred.argmax()]
        cv2.rectangle(frame, (0, 0), (300, 40), (0, 165, 255), -1)

        if prediction_label == 'blank':
            cv2.putText(frame, " ", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        else:
            accu = "{:.2f}".format(np.max(pred) * 100)
            cv2.putText(frame, f'{prediction_label}  {accu}%', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
