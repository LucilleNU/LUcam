.. LUcam documentation master file, created by
   sphinx-quickstart on Tue May  9 17:36:08 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to LUcam's documentation!
=================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

$Project
========

$LUcam will solve your worries and security concerns in your home and personal surroundings. 
It provides an average human being, a viable, simple, and cost-effective solution to security.

This application is designed to be highly responsive, being a PWA it is accessible on several browsers such as Chrome, Firefox, and Safari!

It could easily be installed with the click of a button and has been designed with the capability to operate on multiple platforms, including IOS, Android, Windows 10, and macOS Catalina following installation.

Features
========
	The system can detect motion in its field of view and differentiate between human motion and other types of motion, such as animals or objects.
	The system can track the detected human motion and follow its movement within the field of view.
	The system can record the detected motion. 
	The system can send notifications to the user(s) when motion is detected.
	The system can support both IOS and Android devices.
	The system can support Chrome, Firefox, and Safari browsers.
	The system allows users to customize the colour themes and modes.

Developed Using
========
OpenCV python library for motion detection, 
Flask for deployment of the PWA 
Background subtraction and frame differecig for Image analysis. 
HAAR feature-based algorithm for effective object detection.
React and good old HTML and CSS were used for the front-end development.
Sqlite and Cloudinary were used as databases. 

Installation
========
Install $project by running:

   cd backend 
   python -m venv venv
   # Mac: source venv/bin/activate
   # windows: source .venv/Scripts/activate
   Python3 main.py

   On a new terminal: 
   cd frontend
   npm install
   npm start


Prerequisites
========

You can install the backend packages by running the command:
   * pip install -r requirements.txt

You can install the frontend packages by running the command:
   * npm install


Usage
========
LUcam is a motion detection PWA that allows users to monitor a particular area 
and receive notifications when motion is detected. In this section, 
we'll cover how the LUcam system functions to detect human motion, track its movement, and customize the settings.

   Implementation
   ========
   The principal objective of this project was to design and implement a surveillance system with the capacity to efficiently detect human motion, 
   inform the user of any intruder, and record footage from the exact moment when motion was detected. The system will function in the manner described below:

     * Capturing & Comparing Stage
      To detect movement, we must begin by capturing live pictures of the area to be monitored and keep them under observation. 
      This was implemented by using a webcam that continuously transmits pictures at a predetermined frame rate. 
      To evaluate the presence of motion in a live stream, we compare the camera's real-time images to one another using background subtraction and frame differencing. 
      These techniques enable us to see the differences between the pixel levels and frames and hence confirm the appearance of motion.

     * Classification Stage
      The human classification stage in the LUcam system is responsible for accurately identifying and classifying the detected motion/object within the camera's view as humans. 
      This is achieved using HAAR cascade classifiers, a machine learning-based approach for object detection.
      The LUcam system uses a pre-trained HAAR cascade classifier specifically designed for human detection. 
      The classifier is trained on a dataset of positive and negative examples to recognize human-like features.
      By using HAAR cascade classifiers for human classification, the LUcam system benefits from their speed and efficiency in detecting humans, making it a suitable choice for real-time applications for security monitoring.

      * Video Storage Stage 
      When the LUcam system detects motion, the frames need to be kept in memory as a video and saved to Cloudinary, a cloud database storage provider. Cloudinary is a popular platform for managing media assets such as images and videos, offering a wide range of features like storage, optimization, and transformation. The process of saving the recorded videos to Cloudinary is as follows:
      	Video recording: When motion is detected, the LUcam system captures a video of the event. 
         This video recording stops and is saved once the app sees no additional movements within the camera's view. 
      	Video processing: Before uploading the video to Cloudinary, the system performs additional video processing tasks such as compression, format conversion, or resizing to optimize storage space and improve the performance of the cloud storage.
      	Authentication and authorization: To ensure secure communication between the LUcam system and Cloudinary, the application uses API keys and access tokens provided. 
         These tokens are used to authenticate and authorize the LUcam system's access to the cloud storage account.
      	Video upload: Once the video has been processed and the system has been authenticated, the video is uploaded to Cloudinary using their API. 
         The API allows interaction with the Cloudinary platform and enables seamless integration with the LUcam system.
      	Video retrieval: After the video has been successfully uploaded to Cloudinary, the url is saved to the video table in SQlite and current user is verified. 
         It can be accessed and viewed by authorized users i.e., registered users through the LUcam application. 
         The system provides an interface for users to search, view, and manage their stored videos.

      By utilizing Cloudinary as the cloud storage provider, the LUcam system can take advantage of its extensive features and scalability while ensuring a secure and reliable storage solution for the recorded videos. Additionally, the use of cloud storage allows for easy accessibility and management of the videos from anywhere with an internet connection, further enhancing the user experience.

      * Notification Stage
      Because the user may want to be notified as soon as an intrusion is detected by the app, the software includes an alert system. If a movement is detected, the user is notified right away, and the intruder is recorded. This was implemented using push notifications. 
      Once the user login and selects yes to receiving notifications, the Lucam app requests access to show notifications.
      Once this has been granted and a motion is detected, users will automatically receive a notification alert. 


Modules
========

LUcam is a motion detection PWA that uses several different modules and technologies to detect and track human motion, record motion, and send notifications. In this section, we'll provide an overview of the main modules and technologies used in LUcam.

   OpenCV
   ========
   OpenCV (Open Source Computer Vision Library) is a computer vision and machine learning software library. LUcam uses OpenCV to detect motion in its field of view, differentiate between human motion and other types of motion, and track the movement of detected human motion within the field of view.
   OpenCV provides several functions and algorithms for motion detection, including background subtraction and frame differencing. These functions and algorithms allow LUcam to detect and track motion with high accuracy.

   React
   ========
   React is a JavaScript library for building user interfaces. LUcam uses React for its front-end, which includes the app's user interface and the logic that controls its behavior.
   React provides a declarative programming model that makes it easy to build complex user interfaces. LUcam uses React to create a responsive and intuitive user interface that allows users to monitor and control the app's behavior.

   SQLite
   ========
   SQLite is a software library that provides a relational database management system. LUcam uses SQLite for local storage, which allows it to store data locally on the user's device.
   SQLite is a lightweight and efficient database management system that is easy to integrate into applications. LUcam uses SQLite to store information about detected motion, recorded video clips, and user preferences.

   Cloudinary
   ========
   Cloudinary is a cloud-based media management solution that provides storage, optimization, and manipulation of images and videos. LUcam uses Cloudinary to store recorded video clips and to provide a scalable and reliable storage solution.
   Cloudinary provides several APIs and SDKs that make it easy to integrate media management functionality into applications. LUcam uses Cloudinary's API to upload, store, and retrieve video clips, and to perform optimization and manipulation tasks.
   That's it! With these modules and technologies working together, LUcam is able to provide a powerful and reliable motion detection and surveillance system for its users. If you want to learn more about how these modules and technologies work together in LUcam, 
   please refer to the "API" section of this documentation.


Customization
========

LUcam allows users to customize the color themes and modes of the app. In this section, we'll cover how to customize the settings in LUcam.

   Color Themes and Modes
   ========
   LUcam provides several color themes and modes for users to choose from. To customize the color theme and mode, navigate to the app's settings.
   From there, you can choose the color theme (6 color options) and mode (light, drak, auto) that you prefer. The available color themes and modes may vary depending on the version of the app and the platform you are using.


API
========

LUcam uses Flask RESTful to provide a robust and flexible API for interacting with the app's functionality. 
In this section, we'll provide an overview of the main endpoints and functionality provided by LUcam's API.

   Endpoints
   ========
   LUcam's API provides several endpoints for interacting with the app's functionality. 
   These endpoints are organized into several categories, including motion detection, video recording, and notifications.

     # Motion Detection Endpoints
      '/video_feed': This endpoint is responsible for showing the video feed and returns information (inform of frames) to the backend.
     
      #Video Recording Endpoints
      '/start-recording': This endpoint starts recording a video clip of detected motion.
      '/stop-recording': This endpoint stops recording a video clip of detected motion.

      #Notification Endpoints
      '/toggle_notification': This endpoint is responsible for toggling notification permissions and access.
      if user has agreed to recieve notifications they will receive one.

Source Code
========
.. _a link: https://github.com/LucilleNU/LUcam

Support
========

If you are having issues, please let me know via email at nawalucille@gmail.com