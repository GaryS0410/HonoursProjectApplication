# Importing necessary extensions
import cv2
from PIL import Image
import numpy as np
from io import BytesIO
from flask_login import current_user
from tensorflow.keras.models import load_model

# Importing necessary application imports
from ..models import *

# Global Varaibles 
# Face classifier loads in frontal facing haar cascade
# Image timestamps is used to keep track of times at which webcam photos were taken
model = load_model('app\ml_models\initalModel.h5')
face_classifier = cv2.CascadeClassifier("app\ml_models\haarcascade_frontalface_default.xml")

# Helper function which is used to pre-process the webcam images. Recolours the image to grayscale
# and resizes it to 48 * 48. Also normalises the image by dividing by 255. Uses the haar cascade to crop
# face from image, however this does not work if the face is not facing front. Otherwise, the whole 
# image is used resulting in a more inaccurate classification.
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

def predictImages(images, is_therapy):
    if is_therapy:
        images = images[1:]

    predictions = model.predict(images)
    classes_X = np.argmax(predictions, axis = 1)

    emotion_names = np.array(['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral'])
    emotion_labels = emotion_names[classes_X]

    emotion_labels = emotion_labels.tolist()
    emotion_names = emotion_names.tolist()
    emotions_count = {}

    for i in emotion_labels:
        if i in emotions_count:
            emotions_count[i] += 1
        else:
            emotions_count[i] = 1

    return(emotions_count, emotion_labels)        

# Function used in order to calculate the overall emotional score of a session. Basically, it counts 
# the amount of positive, neutral, and negative emotions and averages which ones were most prevalent.
def calculateEmotionScore(emotions_count):
    positive_emotions = ['happy']
    neutral_emotions = ['surprise', 'disgust', 'neutral']
    negative_emotions = ['fear', 'angry', 'sad']

    positive_count = 0
    neutral_count = 0
    negative_count = 0

    for emotion, count in emotions_count.items():
        if emotion in positive_emotions:
            positive_count += count
        elif emotion in neutral_emotions:
            neutral_count += count
        elif emotion in negative_emotions:
            negative_count += count
    
    total_count = positive_count + neutral_count + negative_count

    if total_count == 0:
        return None
     
    positive_percentage = positive_count / total_count
    neutral_percentage = neutral_count / total_count
    negative_percentage = negative_count / total_count

    if positive_percentage > neutral_percentage and positive_percentage > negative_percentage:
        return 'Positive'
    elif neutral_percentage > positive_percentage and neutral_percentage > negative_percentage:
        return 'Neutral'
    else:
        return 'Negative'

# PHQ-9 Scoreing function
def phq9Score(score):
    if score >= 0 and score <= 4:
        message = "Your most recent PHQ-9 score suggests you have minimal levels of depression."
    elif score >= 5 and score <= 9:
        message = "Your most recent PHQ-9 score suggests you have may mild depression."
    elif score >= 10 and score <= 14:
        message = "Your score suggests you have have moderate depression. It would be beneficial to seek psychiatric treatmeant."
    else:
        message = "Your score suggests you have severe depression. Please seek psychiatric treatment as soon as possible."
    return message

# A function which saves the session data to the database for the patient and therapist user to 
# look at later on. Used to be included within the endpoint, but the PHQ-9 quiz also makes use of
# that function now, which is not saved to any database currently and is not involved in the 
# therapy session data at all.
def saveSessionData(emotional_score, emotion_list, image_timestamps):
    session_db = SessionData(user_id = current_user.id, emotional_score = emotional_score)
    db.session.add(session_db)
    db.session.commit()

    print(emotion_list)
    print(len(image_timestamps))

    for i, emotion in enumerate(emotion_list):
        emotion_db = EmotionData(emotion_type = emotion, time_captured = image_timestamps[i], session_id = session_db.id)
        db.session.add(emotion_db)
    db.session.commit()