# Necessary extension imports
from flask import render_template, request, jsonify, flash, redirect, url_for
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
import cv2
from io import BytesIO
from flask_login import login_required, current_user
from datetime import datetime

# Necessary application imports
from app.models import SessionData, EmotionData
from app.main import bp
from .forms import PHQ9Form
from ..models import User
from .helpers import *

# Necessary global variable declartions
# The image_list variable is used to intialise a empty 4D numpy array which will be used to store
# the webcam images. Is necessary to be a global variable due to multiple endpoint functions
# needing access to it.
# The mode variable makes use of the load_model function in order to load in the created machine
# learning model from the ml_models folder.
image_list = np.zeros((1, 48, 48, 1))
model = load_model('app\ml_models\initalModel.h5')

# Endpoint Functions

# Route for the root of the application and the first page the user sees. If the user is a patient
# they will be directer to the webcam with the ability to start and stop a session, whereas a
# therapist user be be directed to the admin dashboard, wherein they will be able to see a list 
# of their associated patients 
@bp.route('/')
@login_required
def index():
    if current_user.is_therapist:
        return redirect(url_for('admin.adminDash'))
    return render_template('index.html', user=current_user)

# The /startSession endpoint, which is used to capture an image from the front-end and append it
# to the global image_list variable. This variable is used by another function to make predictions
# on the images captured.
@bp.route('/startSession', methods = ['GET', 'POST'])
def startSession():
    global image_list
    if request.method == 'POST':
        fs = request.files.get('snap').read()
        if fs:
            fs = preprocessImage(fs)
            image_list = np.concatenate((image_list, fs), axis = 0)
            current_time = datetime.now()
            image_timestamps.append(current_time)
            return 'Photo captured.' 
        else:
            return 'Could not capture photo.'

# The /predict endpoint. The predict_emotion function is used to make predictions on all images
# contained within the image_list variable. Note: currently the first image is being removed due to 
# the fact that the front-end function takes a picture when the button is pressed originally,
# which we do not want.
@bp.route('/predict', methods = ['GET'])
def predict_emotion():
    if request.method == 'GET':
        global image_list
        image_list = image_list[1:]

        predictions = model.predict(image_list)
        classes_x = np.argmax(predictions, axis = 1)

        emotionNames = np.array(['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral'])
        emotionLabels = emotionNames[classes_x]

        emotion_list = emotionLabels.tolist()
        emotionNames = emotionNames.tolist()
        emotions_count = {}

        for i in emotion_list:
            if i in emotions_count:
                emotions_count[i] += 1
            else: 
                emotions_count[i] = 1
    
        emotional_score = calculateEmotionScore(emotions_count)
        saveSessionData(emotional_score, emotion_list)

        flash('Session data has been saved', category='success')

        image_list = np.zeros((1, 48, 48, 1))
        image_timestamps = []

        return jsonify({'emotions_count': emotions_count, 'emotional_score': emotional_score})

# /quizPredict endpoint, virtually identical to the /predict endpoint except currently used
# for the PHQ-9 quiz functionality. It would be good if these could instead be combined into 
# one function
@bp.route('/quizPredict', methods=['GET', 'POST'])
def predictQuiz():
    if request.method == 'GET':
        global image_list
        predictions = model.predict(image_list)
        classes_x = np.argmax(predictions, axis = 1)

        emotionNames = np.array(['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral'])
        emotionLabels = emotionNames[classes_x]

        emotion_list = emotionLabels.tolist()
        emotionNames = emotionNames.tolist()
        emotions_count = {}

        for i in emotion_list:
            if i in emotions_count:
                emotions_count[i] += 1
            else: 
                emotions_count[i] = 1
        
        image_list = np.zeros((1, 48, 48, 1))

        print(emotions_count)

        return jsonify(emotions_count=emotions_count)

# Endpoint for capturing images for the PHQ-9 quiz. Once again, very similiar to 
# route for therapy session, would be beneficial if they could be combined into one
# thing.
@bp.route('/quizGet', methods=['POST'])
def getQuiz():
    if request.method == 'POST':
        global image_list
        fs = request.files.get('snap').read()
        if fs: 
            fs = preprocessImage(fs)
            image_list = np.concatenate((image_list, fs), axis = 0)
            return "Photo capturing"
        else:
            return "Could not captured photo"

# Route for handling the form subimssion of the PHQ-9 quiz. Also uses logic defined 
# in forms.py for calculating the PHQ-9 score.
@bp.route('/questionnaire', methods = ['GET', 'POST'])
def PHQ9_Questionnaire():
    form = PHQ9Form()
    if form.validate_on_submit():
        score = form.calculate_score()
        print(f"Your score is: {score}")
        flash(f"Your score is: {score}")
        print(score)
        user = User.query.get(current_user.id)
        user.phq9_score = score
        db.session.commit()
        return render_template('PHQ-9.html', form = form, score = score)
    else:
        print(form.errors)
    return render_template('PHQ-9.html', form = form, score = None)

@bp.route('/testRoute')
def testPage():
    return render_template('testPage.html')