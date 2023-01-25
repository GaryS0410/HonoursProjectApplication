from app import app
from flask import Flask, render_template, request, Response, jsonify, make_response
import numpy as np
import json
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import load_img
import cv2
import os
from io import BytesIO
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt

image_list = np.zeros((1, 48, 48, 1))
emotions_count = {}
model = load_model('app\models\initalModel.h5')
face_classifier = cv2.CascadeClassifier("app\models\haarcascade_frontalface_default.xml")

@app.route('/')
def index():
    return render_template('index.html')

# def preprocessImage(webcamImage):
#     webcamImage = Image.open(BytesIO(webcamImage))

#     webcamImage = webcamImage.convert("L")

#     webcamImage = webcamImage.resize((48, 48), resample=Image.BICUBIC)

#     image_array = np.array(webcamImage)
#     image_array = image_array.astype('float32')
#     image_array /= 255.0

#     image_array = np.expand_dims(image_array, axis = 0)
#     image_array = np.expand_dims(image_array, axis = -1)
        
#     return image_array

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

@app.route('/startSession', methods = ['GET', 'POST'])
def startSession():
    if request.method == 'POST':
        fs = request.files.get('snap').read()
        if fs:
            global image_list
            fs = preprocessImage(fs)
            image_list = np.concatenate((image_list, fs), axis = 0)
            return ('got photo')                
        else:
            return 'no photo'
    return render_template('index.html')

@app.route('/predict', methods = ['GET'])
def predict_emotion():
    if request.method == 'GET':
        global image_list
        global emotions_count

        predictions = model.predict(image_list)
        classes_x = np.argmax(predictions, axis = 1)

        emotionNames = np.array(['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral'])
        emotionLabels = emotionNames[classes_x]

        emotion_list = emotionLabels.tolist()
        emotionNames = emotionNames.tolist()
        
        for i in emotion_list:
            if i in emotions_count:
                emotions_count[i] += 1
            else: 
                emotions_count[i] = 1 

        print(emotions_count)

        return jsonify(emotions_count)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/student')
def student():
    return render_template('student.html')