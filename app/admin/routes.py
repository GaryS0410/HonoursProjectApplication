from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import and_
from datetime import datetime

from app import db
from app.models import *
from app.admin import bp
from .helpers import *

############################
# ADMIN ENDPOINT FUNCTIONS #
############################

@bp.route('/adminDashboard')
@login_required
def adminDash():
    if(current_user.is_therapist):
        therapist = current_user
        associations = Association.query.filter_by(therapist_id=therapist.id).all()
        patients = []
        for association in associations:
            patient = User.query.filter_by(id=association.patient_id).first()
            patients.append(patient)
        return render_template('admin/adminDashboard.html', patients=patients, therapist = therapist.first_name)
    else:
        return "<h4> Not authorised </h4>"

@bp.route('/patientOverview/<int:user_id>')
@login_required
def patientData(user_id):
    if(current_user.is_therapist):
        patient = User.query.filter_by(id = user_id).first()
        allSessions = SessionData.query.filter_by(user_id = patient.id).all()
        mostRecentSession = SessionData.query.filter_by(user_id = patient.id).order_by(SessionData.time_of_session.desc()).first()

        emotions_count = {}
        for emotion in mostRecentSession.emotion_data:
            if emotion.emotion_type in emotions_count:
                emotions_count[emotion.emotion_type] += 1
            else: 
                emotions_count[emotion.emotion_type] = 1
        return render_template('admin/patientDetails.html', patient = patient, allSessions = allSessions, mostRecentSession = mostRecentSession, recentSessionEmotions = emotions_count)
    else:
        return "<h4> Not authorised buddy </h4>"

@bp.route('/specificSession/<int:id>')
@login_required
def specificSession(id):
    if(current_user.is_therapist):
        session = SessionData.query.get(id)

        emotional_score = session.emotional_score
        emotion_data = EmotionData.query.filter_by(session_id = session.id).all()
        emotions_count = {}

        for emotion in session.emotion_data:
            if emotion.emotion_type in emotions_count:
                emotions_count[emotion.emotion_type] += 1
            else:
                emotions_count[emotion.emotion_type] = 1

        return render_template('admin/specificSession.html', session = session, score=emotional_score, emotion_data = emotion_data, emotions_count = emotions_count)
    else:
        return "<h4> Not authorised </h4>"


@bp.route('/adminDashboard/deletePatient/<int:patient_id>', methods=['POST'])
@login_required
def deleting_patient(patient_id):
    if (current_user.is_therapist):
        delete_patient(patient_id)
        return redirect(url_for('admin.adminDash'))
    else:
        return "<h4> Not authorised to perform this operation. </h4>"
    
@bp.route('/deleteSession/<int:session_id>', methods = ['GET', 'POST'])
def deleteSession(session_id):
    if(current_user.is_therapist):
        session = SessionData.query.get(session_id)
        if session:
            EmotionData.query.filter_by(session_id = session_id).delete()

            db.session.delete(session)
            db.session.commit()
            
            flash('Session deleted', 'success')
        else:
            flash('Session could not be deleted', 'error')
        # return(url_for('admin.patientData', user_id = session.user_id))
        return redirect(url_for('admin.adminDash'))
    else:
        return "<h4> Not authorised </h4>"