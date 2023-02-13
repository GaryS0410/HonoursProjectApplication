from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Association(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    therapist_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class EmotionData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emotion_type = db.Column(db.String(20), nullable=False)
    emotion_instances = db.Column(db.Integer, nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('session_data.id'))

class SessionData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_of_session = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    emotion_data = db.relationship('EmotionData')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(150))
    is_therapist = db.Column(db.Boolean)
    session_data = db.relationship('SessionData')
    patients = db.relationship('Association', foreign_keys = [Association.therapist_id], backref='therapist')
    therapist = db.relationship('Association', foreign_keys=[Association.patient_id], backref='patient', uselist=False)