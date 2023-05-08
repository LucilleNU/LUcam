#!/usr/bin/env python3
"""
What is this module for?
"""
import cv2
import time
import datetime
from plyer import notification
from PIL import Image

from flask_socketio import SocketIO, emit
from flask import Flask
from io import StringIO,BytesIO
from base64 import b64decode,b64encode
import numpy as np
import logging
from time import sleep
import hashlib
import requests


from flask_cors import CORS
import imutils
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')

import cloudinary

from cloudinary.uploader import unsigned_upload,upload
from cloudinary.utils import cloudinary_url

cloudinary.config(
  cloud_name = "dq4l61m3h",
  api_key = "637113654295649",
  api_secret = "dfS0OYl-ajvj4gIFheuqzDl10x0",
)
api_secret="dfS0OYl-ajvj4gIFheuqzDl10x0"
video_path = './output_video.mp4'
public_id = 'samples/output_video'

timestamp = str(int(time.time()))
signature = hashlib.sha1(f"timestamp={timestamp}{api_secret}".encode('utf-8')).hexdigest()

url = 'https://api.cloudinary.com/v1_1/dq4l61m3h/video/upload'
files = {'file': open('./output_video.mp4', 'rb')}
auth_data = {
    'api_key':  "637113654295649",
    'timestamp': timestamp,
    'signature': signature
}
response = requests.post(url, files=files,data=auth_data)
if response.status_code == 200:
    print('Upload successful.')
else:
    print('Upload failed.')

def motion(pimg):
    cap = cv2.cvtColor(pimg, cv2.COLOR_RGB2BGR)    
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    fullbody_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_fullbody.xml")
    eye_cascade = cv2.CascadeClassifier
    (cv2.data.haarcascades + "haarcascade_eye.xml")

    detection = False
    detection_stopped_time = None
    timer_started = False
    SECONDS_TO_RECORD_AFTER_DETECTION = 5
    
    frame_size = (400, 300)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = None
    times = []

    notification_enabled = False
    notifications_allowed = False


    def show_notification():
        notification.notify(
            title='Motion Detected!!',
            message='Login to view video of intruder',
            timeout=5
        )


    def gen():
        while True:
            global notification_enabled
            ret, frame = cap.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            bodies = fullbody_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) + len(bodies) > 0:
                global detection
                if detection:
                    global timer_started
                    timer_started = False
                else:
                    detection = True
                    now = datetime.datetime.now()
                    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
                    global out
                    out = cv2.VideoWriter(
                        f"{current_time}.mp4", fourcc, 20, frame_size)
                    print("Started Recording!")
                    cv2.putText(frame, "Motion Detected",
                                (10, 70), cv2.FONT_HERSHEY_SIMPLEX,
                                2, (0, 0, 255), 3)
                    # Show a notification when motion is detected
                    print(notification_enabled)
                    print(notifications_allowed)
                    if notification_enabled:
                        show_notification()
            elif detection:
                if timer_started:
                    global detection_stopped_time
                    current_time = time.time()
                    subtracted_time = current_time - detection_stopped_time
                    if subtracted_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                        detection = False
                        timer_started = False
                        out.release()
                        # mail()
                        print('Stop Recording!')
                else:
                    timer_started = True
                    detection_stopped_time = time.time()

            if detection:
                out.write(frame)

            frame = cv2.imencode('.jpg', frame)[1].tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            

            
def base64_to_image(base64_string):
    # Extract the base64 encoded binary data from the input string
    base64_data = base64_string.split(",")[1]
    # Decode the base64 data to bytes
    image_bytes = b64decode(base64_data)
    # Convert the bytes to numpy array
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    # Decode the numpy array as an image using OpenCV
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image

frames = []

@socketio.on('connect')
def handleConnect():
    print("UI connected")
    

    
@socketio.on('disconnect')
def handleConnect():
    print("UI Disconnected")


@socketio.on("image")
def receive_image(image):
    try:
        # Convert the base64-encoded image to a numpy array
        image = base64_to_image(image)

        # Perform image processing using OpenCV
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Add the processed frame to the list of frames
        frames.append(gray)

        # Send the processed image back to the client
        encoded_img = cv2.imencode('.jpg', gray)[1]
        b64_src = "data:image/jpeg;base64,"
        processed_img_data = b64_src + b64encode(encoded_img).decode()
        emit("processed_image", processed_img_data)

    except Exception as e:
        # Log the exception
        logging.error("An error occurred: %s", str(e))

@socketio.on("merge-processed")
def merge_and_upload():
    output_file = 'output_video.mp4'

    # Define the video codec (MP4V) and output video dimensions
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    height, width = frames[0].shape[:2]
    video = cv2.VideoWriter(output_file, fourcc,30, (width, height))

    # Iterate over each frame and write it to the video
    for frame in frames:
        # Convert the frame format to BGR if necessary
        if len(frame.shape) == 2:
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        else:
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Write the frame to the video
        video.write(frame_bgr)

    video.release()
    response = unsigned_upload(
    video_path,
    'jzfnfrsi',
     cloud_name = "dq4l61m3h",
  api_key = "637113654295649",

    timestamp=timestamp,
    signature=signature,
    resource_type='video'
    
)
    # Send the video file to the specified URL using an HTTP POST request
    
    video_url = response['secure_url']
    base_url, video_id = video_url.rsplit('/', 1)

    # Add 'q_auto' parameter after 'upload' in the base URL
    modified_url = base_url + '/q_auto/' + video_id
    print(f"Video uploaded successfully. URL: {modified_url}")

frames = []

if __name__ == '__main__':
    socketio.run(app, debug=True, port=8000)
