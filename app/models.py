from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Association(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    therapist_id = db.Column(db.Integer, db.ForeignKey('therapist.id'))

class EmotionData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emotion_type = db.Column(db.String(20), nullable=False)
    time_captured = db.Column(db.DateTime(timezone=True), default=func.now())
    session_id = db.Column(db.Integer, db.ForeignKey('session_data.id'))

class SessionData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time_of_session = db.Column(db.DateTime(timezone=True), default=func.now())
    emotional_score = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    emotion_data = db.relationship('EmotionData')

class User(db.Model, UserMixin):
    __tablename = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(150))
    is_therapist = db.Column(db.Boolean)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': is_therapist
    }

class Patient(User):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    phq9_score = db.Column(db.Integer)
    session_data = db.relationship('SessionData')
    therapist = db.relationship('Association', foreign_keys = [Association.therapist_id], backref='therapist')

    __mapper_args__ = {
        'polymorphic_identity': 'patient'
    }

class Therapist(User):
    __tablename__ = 'therapist'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    patients = db.relationship('Association', foreign_keys=[Association.patient_id], backref='patient', uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': 'therapist'
    }