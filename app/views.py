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

img_counter = 0
image_list = np.zeros((1, 48, 48, 1))
model = load_model('app\models\initalModel.h5')

@app.route('/')
def index():
    return render_template('index.html')

def preprocessImage(webcamImage):
    webcamImage = Image.open(BytesIO(webcamImage))

    webcamImage = webcamImage.convert("L")
    webcamImage = webcamImage.resize((48, 48), resample=Image.BICUBIC)

    image_array = np.array(webcamImage)
    image_array = image_array.astype('float32')
    image_array /= 255.0

    image_array = np.expand_dims(image_array, axis = 0)
    image_array = np.expand_dims(image_array, axis = -1)
        
    return image_array

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
        class_prediction = model.predict(image_list)
        classes_x = np.argmax(class_prediction, axis = 1)
        emotion = np.array(['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral'])
        emotions = emotion[classes_x]
        print(emotions, class_prediction)
        emotion_list = emotions.tolist()
        json_str = json.dumps(emotion_list)
        return json_str

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/student')
def student():
    return render_template('student.html')