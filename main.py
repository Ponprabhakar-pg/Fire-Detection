import cv2
import numpy
from flask import Flask, render_template, Response, stream_with_context, request
import winsound





fire_cascade = cv2.CascadeClassifier('fire_detection.xml')
video = cv2.VideoCapture(0)
app = Flask('__name__')


# def video_stream():
#     while True:
#         ret, frame = video.read()
#         if not ret:
#             break;
#         else:
#             ret, buffer = cv2.imencode('.jpeg',frame)
#             frame = buffer.tobytes()
#             yield (b' --frame\r\n' b'Content-type: imgae/jpeg\r\n\r\n' + frame +b'\r\n')


@app.route('/camera')
def camera():
    return render_template('camera.html')


@app.route('/')
def start():
    return "welcome "


@app.route('/stop')
def stop():
    print("Trigger Extinguisher")
    return "true"

@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


def video_stream():
    while True:
        ret, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fire = fire_cascade.detectMultiScale(frame, 1.2, 5)

        for (x, y, w, h) in fire:
            cv2.rectangle(frame, (x - 20, y - 20), (x + w + 20, y + h + 20), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            print("fire is detected")
            # duration = 1000  # milliseconds
            # freq = 440  # Hz
            # winsound.Beep(freq, duration)

        if not ret:
            break;
        else:
            ret, buffer = cv2.imencode('.jpeg',frame)
            frame = buffer.tobytes()
            yield (b' --frame\r\n' b'Content-type: imgae/jpeg\r\n\r\n' + frame +b'\r\n')

app.run(host='127.0.0.1', port='5000', debug=False)