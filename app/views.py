from app import app
from flask import Flask, render_template, request, Response, jsonify, make_response
import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import load_img
import os
from werkzeug.utils import secure_filename


img_counter = 0
image_list = np.array([])
model = load_model('app\models\initalModel.h5')

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        fs = request.files.get('snap')
        if fs:
            global image_list
            image = Image.open(fs)
            image_list = np.append(image_list, image)
            print(len(image_list))
            return 'got photo'
        else:
            return 'no photo'
    return render_template('index.html')

def read_image(filename):        
    img = load_img(filename, grayscale = True, target_size = (48, 48), keep_aspect_ratio = True)
    x = image.img_to_array(img)

    x = np.expand_dims(x, axis = 0)
    x = x.reshape(1, 48, 48, 1)

    x /= 255.0

    x = x.astype('float32')
    x = x.reshape(1, 48, 48, 1)
    return x

@app.route('/predict', methods = ['GET'])
def predict_emotion():
    if request.method == 'GET':
        image_list = read_image(image_list)
        class_prediction = model.predict(image_list)
        classes_x = np.argmax(class_prediction, axis = 1)
        if classes_x == 0:
            emotion = 'angry'
        elif classes_x == 1:
            emotion = 'disgust'
        elif classes_x == 2:
            emotion = 'fear'
        elif classes_x == 3:
            emotion = 'happy'
        elif classes_x == 4:
            emotion = 'sad'
        elif classes_x == 5:
            emotion = 'surprise'
        elif classes_x == 6:
            emotion = 'neutral'
        return render_template('index.html', emotion = emotion, prob = class_prediction)

@app.route('/about')
def about():
    return "<h1 style='color: red'> About Page </h1>"