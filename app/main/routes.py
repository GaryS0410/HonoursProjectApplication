# Necessary extension imports
from flask import render_template, request, jsonify, redirect, url_for
import numpy as np
from flask_login import login_required, current_user
from datetime import datetime

# Necessary application imports
from app.main import bp
from .forms import PHQ9Form
from ..models import User
from .helpers import *

# Global variabels
image_list = np.zeros((1, 48, 48, 1))
quiz_image_list = np.zeros((1, 48, 48, 1))
image_timestamps = []

# Endpoint Functions

# Route for root of application
@bp.route('/')
@login_required
def index():
    if current_user.is_therapist:
        return redirect(url_for('admin.adminDash'))
    return render_template('index.html', user=current_user)

# /startSession endpoint, takes images for therapy sessions
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

# The /predict endpoint, used to predict on therapy images
@bp.route('/predict', methods=['GET'])
def predict():
    if request.method == 'GET':
        global image_list
        global image_timestamps

        is_therapy = True
        emotions_count, emotion_labels = predictImages(image_list, is_therapy)
        emotional_score = calculateEmotionScore(emotions_count)

        saveSessionData(emotional_score, emotion_labels, image_timestamps)

        image_list = np.zeros((1, 48, 48, 1))
        image_timestamps = []

        return jsonify({'emotions_count': emotions_count, 'emotional_score': emotional_score})

@bp.route('/predictQuiz', methods=['GET'])
def predictQuiz():
    global quiz_image_list

    is_therapy = False
    emotions_count, emotions_labels = predictImages(quiz_image_list, is_therapy)
    quiz_image_list = np.zeros((1, 48, 48, 1))

    return emotions_count

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
            return "Could not  photo"

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

@bp.route('/resources')
def resource_page():
    return render_template('resources.html')