from flask import Blueprint, render_template, request, jsonify, flash
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
import cv2
from io import BytesIO
from flask_login import login_required, current_user

from . import db
from .models import SessionData, EmotionData

# Views.py blueprint declaration
views = Blueprint('views', __name__)

# GLOBAL VARIABLES
image_list = np.zeros((1, 48, 48, 1))
model = load_model('app\ml_models\initalModel.h5')
face_classifier = cv2.CascadeClassifier("app\ml_models\haarcascade_frontalface_default.xml")


# HELPER FUNCTIONS
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

# ENDPOINT FUNCTIONS
@views.route('/')
@login_required
def index():
    return render_template('index.html', user=current_user)

@views.route('/startSession', methods = ['GET', 'POST'])
def startSession():
    global image_list
    if request.method == 'POST':
        fs = request.files.get('snap').read()
        if fs:
            fs = preprocessImage(fs)
            image_list = np.concatenate((image_list, fs), axis = 0)
            return 'got photo'       
        else:
            return 'no photo'

@views.route('/predict', methods = ['GET'])
def predict_emotion():
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

        session_db = SessionData(user_id = current_user.id)
        db.session.add(session_db)
        db.session.commit()

        for emotion_name, count in emotions_count.items():
            emotion_db = EmotionData(emotion_type = emotion_name, emotion_instances=count, session_id = session_db.id)
            db.session.add(emotion_db)
        db.session.commit()

        print(emotions_count)

        flash('Session data has been saved', category='success')

        image_list = np.zeros((1, 48, 48, 1))
        return jsonify(emotions_count)

@views.route('/previous')
@login_required
def displayPreviousData():
    sessions = SessionData.query.filter_by(user_id = current_user.id).all()
    session_data = []
    for session in sessions:
        emotions_count = {}
        for emotion in session.emotion_data:
            emotions_count[emotion.emotion_type] = emotion.emotion_instances
        session_data.append({"session_id": session.id, "emotions_count": emotions_count}) 
    return render_template('previousSessions.html', sessions = sessions , session_data=session_data)