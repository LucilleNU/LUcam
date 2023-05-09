#!/usr/bin/env python3

"""
What is this module for?
"""

import logging
from contextlib import _RedirectStream
import datetime
import unittest
import cv2
from flask import Flask, redirect,render_template, Response, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
# from camera import gen
# from camera import fourcc
# from camera import frame_size
# import camera
import os
import psycopg2
from dotenv import load_dotenv
from version import __version__
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import sqlite3


logging.debug("Version:", __version__)
load_dotenv()  # loads variables from .env file into environment

from flask import Flask,jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey' # Set a secret key for Flask sessions  

db = SQLAlchemy(app)  # gets variables from environment

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

current_user_username = ''

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    video_urls = db.Column(db.String(200))  # New column for video URLs

class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    
    email = StringField(validators=[
                           InputRequired(), Length(min=8, max=40)], render_kw={"placeholder": "Email"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

@app.route('/')


@app.route('/dashboard', methods=['GET', 'POST'])
# @login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    formUsername = data['username']
    formPpassword = data['password']
    user = User.query.filter_by(username=formUsername).first()
    if user:

        if bcrypt.check_password_hash(user.password, formPpassword):
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute('INSERT INTO current_user (username) VALUES (?)', (user.username,))
            conn.commit()
            conn.close()
            response = jsonify({'message': 'Login successful'})
            response.status_code = 200
            response = jsonify({'message': 'Login successful'})
            response.status_code = 200
        else:
            response = jsonify({'message': 'Invalid password'})
            response.status_code = 401  # Unauthorized
    else:
        response = jsonify({'message': 'User not found'})
        response.status_code = 404  # Not Found
    return response    
    
@app.route('/recordings',methods=['GET'])
def recordings():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT username FROM current_user ORDER BY id DESC LIMIT 1')
    current_user = cur.fetchone()
    print(current_user)
    cur.execute('SELECT url FROM videos WHERE username = ?', (current_user[0],))
    result = cur.fetchall()
    print("RESULT:", result)

    conn.close()
    data = {'data': result}
    return jsonify(data)
    
@app.route('/register', methods=['POST'])
def register():
    
    data = request.json
    username = data['username']
    email = data['email']
    password = data['password']
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    try:
        db.session.commit()
        response = jsonify({'message': 'Registration successful'})
        response.status_code = 200
    except Exception as e:
        db.session.rollback()
        response = jsonify({'message': 'Registration failed'})
        response.status_code = 500  # Internal Server Error
    
    return response


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# @app.route('/video_feed')
# def video_feed():
#     """
#     This function is responsible for showing the video feed
#     """
#     return Response(gen(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start-recording', methods=['POST'])
def start_recording():
    """
    This function is responsible for recording the motion
    """
    global detection, out

    if not detection:
        detection = True
        current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        out = cv2.VideoWriter(f"{current_time}.mp4", fourcc, 20, frame_size)
        logging.debug("Started Recording!")

    return "Recording started"


@app.route('/stop-recording', methods=['POST'])
def stop_recording():
    """
    This function is responsible for stopping the recording
    once motion is detected
    """
    global detection, out
    if detection:
        detection = False
        out.release()
        logging.debug('Stopped Recording and Saved Video')
    return _RedirectStream('/')


@app.route('/toggle_notification', methods=['POST'])
def toggle_notification():
    """
    This function is responsible for toggling notification permissions and access.
    """
    status = request.form.get('status')
    permission = request.form.get('permission')
    print(status)
    print(permission)
    
    response_data = {
        'message': 'Notification settings updated',
        'status': status,
        'permission': permission
    }
    
    return jsonify(response_data), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)