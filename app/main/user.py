# Necessary extension imports
from flask import render_template
from flask_login import login_required, current_user

# Necessary imports from the application
from app.models import SessionData, EmotionData
from app.main import bp
from .helpers import phq9Score
from ..models import User

# /profile endpoint which is used to display the users profile to them.
# Queries the database for all the users sessions, most recent session, and most
# recent emotions count during session. Most recent session and emotions count are 
# used to construct the most recent session pie chart whereas all sessions is used
# to populate the datatable
@bp.route('/profile')
@login_required
def profile():
    patient = User.query.filter_by(id = current_user.id).first()
    allSessions = SessionData.query.filter_by(user_id = patient.id).all()

    mostRecentSession = SessionData.query.filter_by(user_id = patient.id).order_by(SessionData.time_of_session.desc()).first()
    message = phq9Score(current_user.phq9_score)

    emotion_score = patient.phq9_emotional_score

    emotions_count = {}
    if mostRecentSession is not None:
        for emotion in mostRecentSession.emotion_data:
            if emotion.emotion_type in emotions_count:
                emotions_count[emotion.emotion_type] += 1
            else:
                emotions_count[emotion.emotion_type] = 1
    return render_template('patientProfile.html', user = patient, allSessions = allSessions, latestSession = mostRecentSession, recentSessionEmotions = emotions_count, 
                           message = message, emotion_score = emotion_score)

# /specific/id endpoint. This allows the user to view the details of a specific session
# such as the emotionals score and all the emotions captured during said session. 
# The timestamps for all the emotions captured is displayed in the datatable.
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

    return render_template('sessionDetails.html', score = emotional_score, emotion_data = emotion_data, emotions_count = emotions_count, session = session)