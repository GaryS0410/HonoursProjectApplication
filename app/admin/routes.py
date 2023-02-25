from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import and_
from datetime import datetime

from app import db
from app.models import *
from app.admin import bp

@bp.route('adminDashboard')
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

@bp.route('/adminDashboard/<int:user_id>')
@login_required
def patientData(user_id):
    patient = User.query.get(user_id)
    sessions = SessionData.query.filter_by(user_id = user_id).all()
    session_data = []
    for session in sessions:
        emotions_count = {}
        for emotion in session.emotion_data:
            emotions_count[emotion.emotion_type] = emotion.emotion_instances
        session_data.append({"session_id": session.id, "emotions_count": emotions_count})

    return render_template('admin/patientDetails.html', sessions = sessions, session_data = session_data, patient=patient)
