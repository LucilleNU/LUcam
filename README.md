# LUcam 

A Progressive Web Application (PWA) for human motion detection. LUcam provided real-time detection, making it a valuable tool for security and surveillance purposes. The application is able to record videos of the detected motion and also notify users of this intrution. This application is designed to be highly responsive, being a PWA it is accessible on several browsers such as Chrome, Firefox, and Safari! 

It could easily be installed with the click of a button and has been designed with the capability to operate on multiple platforms, including IOS, Android, Windows 10, and macOS Catalina following installation.

# Prerequisites<br/>
You can install the backend packages by running the command: <br/>
* `pip install -r requirements.txt` <br/>
You can install the frontend packages by running the command: <br/>
* `npm install`

# Run Application 
* `cd backend ` <br/>
* `python -m venv venv`<br/>
Mac: 
* `source venv/bin/activate` <br/>
windows: 
* `source .venv/Scripts/activate` <br/>
* `Python3 main.py` <br/>

On a new terminal <br/>
* `cd frontend` <br/>
* `npm install` <br/>
* ` npm start`<br/>


# Built With
This was developed using: <br/>

OpenCV Python for motion detection. <br/>
Flask for deployment to the web server.<br/>
React for frontend development <br/>
Haar Cascade Classifier algorithm for effective object detection<br/>

# Tested With
The application has gone through several tests, pytest using assertions, usability test and unit tests. <br/>

## main.py
The main.py has been tested using pytest, it uses the client fixture to make requests to the Flask app and then makes assertions about the response. For example, the test_index test makes a GET request to the root URL ('/') and then asserts that the response status code is 200. Similarly, the test_video_feed test makes a GET request to the /video_feed endpoint and asserts that the response status code is 200 and the content type is 'multipart/x-mixed-replace; boundary=frame'.

## camera.py
The camera tests checks the functionality of the motion detection. This was also done using pytest and mock library for mocking the notify function and the video capture object. it uses fixtures to create a fake video capture object for testing which makes it easy to set up the necessary environment for proper testing.

## Test Coverage
The Lucam app has a test covergae of 90% which means it is reliable and robust, and that most of the potential issues have been identified and addressed.