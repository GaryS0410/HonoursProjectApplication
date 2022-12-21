from app import app
from flask import Flask, render_template, request, Response, jsonify, make_response
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import load_img
import os
from werkzeug.utils import secure_filename

img_counter = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/saveImage', methods = ['GET', 'POST'])
def uploadImage():
    global img_counter
    if request.method == 'POST':
        fs = request.files.get('snap')
        if fs:
            print('FileStorage', fs)
            print('Filename', fs.filename)
            fs.save('uploaded_images/image_{}.jpeg'.format(img_counter))
            img_counter += 1
            return 'got photo'
        else:
            return 'no photo'

@app.route('/about')
def about():
    return "<h1 style='color: red'> About Page </h1>"