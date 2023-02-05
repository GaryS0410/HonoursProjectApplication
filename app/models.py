from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.types import PickleType
import json

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
    session_data = db.relationship('SessionData')