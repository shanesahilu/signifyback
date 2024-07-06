from flask import Flask, render_template, Response, jsonify
from realtimedetection import VideoCamera

app = Flask(__name__)
video_camera = VideoCamera()
last_prediction = {"label": "", "accuracy": ""}

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    global last_prediction
    while True:
        frame, prediction = camera.get_frame()
        last_prediction = prediction
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(video_camera), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/prediction')
def prediction():
    return jsonify(last_prediction)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
