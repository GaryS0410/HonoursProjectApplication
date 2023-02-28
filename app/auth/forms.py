from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app.models import User

class RegisterPatientForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2)], render_kw={"placeholder": "Enter your first name..."})
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2)], render_kw={"placeholder": "Enter your surname..."})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email..."})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=7)], render_kw={"placeholder": "Enter your password..."})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm your password..."})
    therapist_choice = SelectField('Therapist', coerce=int, validators=[DataRequired()], render_kw={"placeholder": "Select therapist..."})
    submit = SubmitField('Sign Up')

    def __init__(self, *args, **kwargs):
        super(RegisterPatientForm, self).__init__(*args, **kwargs)

        therapist_list = User.query.filter_by(is_therapist=True).all()
        if therapist_list:
            self.therapist_choice.choices = [(therapist.id, f"{therapist.first_name} {therapist.surname}") 
                                         for therapist in User.query.filter_by(is_therapist=True).all()]
        else: 
            self.therapist_choice.choices = [(0, "No Therapists Currently Available.")]

class RegisterTherapist(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2)], render_kw={"placeholder": "Enter your first name..."})
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2)], render_kw={"placeholder": "Enter your surname..."})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter your email..."})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=7)], render_kw={"placeholder": "Enter your password..."})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm your password..."})
    submit = SubmitField('Sign Up')