from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
import cv2
from io import BytesIO
from flask_login import login_required, current_user
from datetime import datetime

from app import db
from app.models import SessionData, EmotionData
from app.main import bp
from .forms import PHQ9Form
from ..models import User

####################
# GLOBAL VARIABLES #
####################
image_list = np.zeros((1, 48, 48, 1))
model = load_model('app\ml_models\initalModel.h5')  
face_classifier = cv2.CascadeClassifier("app\ml_models\haarcascade_frontalface_default.xml")
image_timestamps = []

####################
# HELPER FUNCTIONS #
####################
def preprocessImage(webcamImage):
    webcamImage = Image.open(BytesIO(webcamImage))
    grey_image = cv2.cvtColor(np.array(webcamImage), cv2.COLOR_BGR2GRAY)

    try:
        face = face_classifier.detectMultiScale(grey_image, scaleFactor=1.3, minNeighbors=5)

        x, y, w, h = face[0]

        face_image = grey_image[y:y+h, x:x+w]

        face_image = cv2.resize(face_image, (48, 48))
        face_image = face_image.astype('float32')
        face_image /= 255.0

        face_image = np.expand_dims(face_image, axis = 0)
        face_image = np.expand_dims(face_image, axis = -1)
        
        return face_image

    except:
        grey_image = cv2.resize(grey_image, (48, 48))
        grey_image = grey_image.astype('float32')
        grey_image /= 255.0

        grey_image = np.expand_dims(grey_image, axis = 0)
        grey_image = np.expand_dims(grey_image, axis = -1)
            
        return grey_image

def calculateEmotionScore(emotions_count):
    postive_emotions = ['happy']
    neutral_emotions = ['surprise', 'disgust', 'neutral']
    negative_emotions = ['fear', 'angry', 'sad']

    postive_count = 0
    neutral_count = 0
    negative_count = 0

    for emotion, count in emotions_count.items():
        if emotion in postive_emotions:
            postive_count += count
        elif emotion in neutral_emotions:
            neutral_count += count
        elif emotion in negative_emotions:
            negative_count += count
    
    total_count = postive_count + neutral_count + negative_count

    if total_count == 0:
        return None
    
    postive_percentage = postive_count / total_count
    neutral_percentage = neutral_count / total_count
    negative_percentage = negative_count / total_count

    if postive_percentage > neutral_percentage and postive_percentage > negative_percentage:
        return 'Postive'
    elif neutral_percentage > postive_percentage and neutral_percentage > negative_percentage:
        return 'Neutral'
    else:
        return 'Negative'

######################
# ENDPOINT FUNCTIONS #
######################

@bp.route('/')
@login_required
def index():
    if current_user.is_therapist:
        return redirect(url_for('admin.adminDash'))
    return render_template('index.html', user=current_user)

@bp.route('/startSession', methods = ['GET', 'POST'])
def startSession():
    global image_list
    global image_timestamps
    if request.method == 'POST':
        fs = request.files.get('snap').read()
        if fs:
            fs = preprocessImage(fs)
            image_list = np.concatenate((image_list, fs), axis = 0)
            print(len(image_list))
            current_time = datetime.now()
            image_timestamps.append(current_time)
            print(len(image_timestamps))
            return 'got photo'   
        else:
            return 'no photo'

@bp.route('/predict', methods = ['GET'])
def predict_emotion():
    if request.method == 'GET':
        global image_list
        global image_timestamps
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

        session_db = SessionData(user_id = current_user.id, emotional_score = emotional_score)
        db.session.add(session_db)
        db.session.commit()

        timestamp = datetime.now()

        for i, emotion in enumerate(emotion_list):
            emotion_db = EmotionData(emotion_type = emotion, time_captured = image_timestamps[i], session_id = session_db.id)
            db.session.add(emotion_db)
        db.session.commit()

        flash('Session data has been saved', category='success')

        image_list = np.zeros((1, 48, 48, 1))

        return jsonify({'emotions_count': emotions_count, 'emotional_score': emotional_score})

@bp.route('/previous')
@login_required
def displayPreviousData():
    sessions = SessionData.query.filter_by(user_id=current_user.id).all()
    session_data = []
    for session in sessions:
        emotions_count = {}
        for emotion in session.emotion_data:
            if emotion.emotion_type in emotions_count:
                emotions_count[emotion.emotion_type] += 1
            else:
                emotions_count[emotion.emotion_type] = 1
        session_data.append({"session_id": session.id, "emotions_count": emotions_count})
    return render_template('previousSessions.html', sessions=sessions, emotion_data=session_data)

@bp.route('/profile')
@login_required
def profile():
    patient = User.query.filter_by(id = current_user.id).first()
    allSessions = SessionData.query.filter_by(user_id = patient.id).all()
    mostRecentSession = SessionData.query.filter_by(user_id = patient.id).order_by(SessionData.time_of_session.desc()).first()

    emotions_count = {}
    for emotion in mostRecentSession.emotion_data:
        if emotion.emotion_type in emotions_count:
            emotions_count[emotion.emotion_type] += 1
        else:
            emotions_count[emotion.emotion_type] = 1
    return render_template('patientProfile.html', user = patient, allSessions = allSessions, latestSession = mostRecentSession, recentSessionEmotions = emotions_count)

@bp.route('/questionnaire', methods = ['GET', 'POST'])
def PH9_Questionnaire():
    questionnaire = PHQ9Form()
    return render_template('PHQ-9.html', form = questionnaire)

@bp.route('/specific/<int:id>')
def specific(id):
    session = SessionData.query.get(id)

    emotional_score = session.emotional_score
    emotions_count = {}
    
    for emotion in session.emotion_data:
        if emotion.emotion_type in emotions_count:
            emotions_count[emotion.emotion_type] += 1
        else:
            emotions_count[emotion.emotion_type] = 1 

    emotion_data = EmotionData.query.filter_by(session_id = session.id).all()

    return render_template('sessionDetails.html', score = emotional_score, emotion_data = emotion_data, emotions_count = emotions_count)