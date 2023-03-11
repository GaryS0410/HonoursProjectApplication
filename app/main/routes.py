# Necessary extension imports
from flask import render_template, request, jsonify, flash, redirect, url_for
import numpy as np
from flask_login import login_required, current_user
from datetime import datetime

# Necessary application imports
from app.main import bp
from .forms import PHQ9Form
from ..models import User
from .helpers import *

# Necessary global variable declartions
# The image_list variable is used to intialise a empty 4D numpy array which will be used to store
# the webcam images. Is necessary to be a global variable due to multiple endpoint functions
# needing access to it.
image_list = np.zeros((1, 48, 48, 1))
quiz_image_list = np.zeros((1, 48, 48, 1))
image_timestamps = []

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
    global image_timestamps
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
@bp.route('/predict', methods=['GET'])
def predict():
    if request.method == 'GET':
        global image_list
        global image_timestamps

        is_quiz = True
        emotions_count, emotion_labels = predictImages(image_list, is_quiz)
        emotional_score = calculateEmotionScore(emotions_count)

        saveSessionData(emotional_score, emotion_labels, image_timestamps)

        image_list = np.zeros((1, 48, 48, 1))
        image_timestamps = []

        return jsonify({'emotions_count': emotions_count, 'emotional_score': emotional_score})

def predictQuiz():
    global quiz_image_list

    is_quiz = False
    emotions_count, emotions_labels = predictImages(quiz_image_list, is_quiz)
    quiz_image_list = np.zeros((1, 48, 48, 1))

    print(emotions_count)
    print(emotions_labels)

    return emotions_count

# Endpoint for capturing images for the PHQ-9 quiz. Once again, very similiar to 
# route for therapy session, would be beneficial if they could be combined into one
# thing.
@bp.route('/quizGet', methods=['POST'])
def getQuiz():
    if request.method == 'POST':
        global quiz_image_list
        fs = request.files.get('snap').read()
        if fs: 
            fs = preprocessImage(fs)
            quiz_image_list = np.concatenate((quiz_image_list, fs), axis = 0)
            return "Photo capturing"
        else:
            return "Could not captured photo"

# Route for handling the form subimssion of the PHQ-9 quiz. Also uses logic defined 
# in forms.py for calculating the PHQ-9 score.
@bp.route('/questionnaire', methods = ['GET', 'POST'])
def PHQ9_Questionnaire():
    form = PHQ9Form()
    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        emotions = predictQuiz()

        score = form.calculate_score()
        phq9_emotional_score = calculateEmotionScore(emotions)
        print(phq9_emotional_score)

        user.phq9_score = score
        user.phq9_emotional_score = phq9_emotional_score

        db.session.add(user)
        db.session.commit()
        return render_template('PHQ-9.html', form = form, score = score, phq9_emotional_score = phq9_emotional_score)
    else:
        print(form.errors)
    return render_template('PHQ-9.html', form = form, score = None)