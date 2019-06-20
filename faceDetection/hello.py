from zumi.util.camera import Camera

from flask import Flask, render_template, Response
import cv2
import socket
import io
import sys

app = Flask(__name__)

@app.route('/')
def index():
   """Video streaming ."""
   return render_template('index.html')

def gen():
    camera = Camera(192, 96, auto_start=True)
    face_detector = cv2.CascadeClassifier("/usr/local/lib/python3.5/dist-packages/zumi/util/src/haarcascade_frontalface_default.xml")
    """Video streaming generator function."""
    while True:
       frame = camera.capture()
       gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
       faces = face_detector.detectMultiScale(gray, 1.2, 5)

       for(x, y, w, h) in faces:
           cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)

       frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

       cv2.imwrite('pic.jpg', frame)
       yield (b'--frame\r\n' 
              b'Content-Type: image/jpeg\r\n\r\n' + open('pic.jpg', 'rb').read() + b'\r\n')

@app.route('/video_feed')
def video_feed():
   """Video streaming route. Put this in the src attribute of an img tag."""
   return Response(gen(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, threaded=True, port=3456)
