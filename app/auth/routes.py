from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import login_user, login_required, logout_user, current_user

from app.auth import bp

# Auth.py blueprint declaration
auth = Blueprint('auth', __name__)

@bp.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category ='sucess')
                print('logged in')
                login_user(user, remember=True)
                return redirect(url_for('main.index'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Account doesn\'t exist', category='error')
            print("no account")

    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/registerChoice')
def registerChoice():
    return render_template('auth/registerChoice.html')

@bp.route('/registerTherapist', methods=['GET', 'POST'])
def registerTherapist():
    if request.method == 'POST':
        first_name = request.form.get('firstname')
        surname = request.form.get('surname')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 1 character.', category='error')
        elif len(first_name) < 2:
            flash('Surname must be greater than 2 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Passwords must be at least 7 characters long.', category='error')
        else:
            new_therapist = User(first_name = first_name, surname = surname, email=email, password=generate_password_hash(password1, method='sha256'), is_therapist = True)
            db.session.add(new_therapist)
            db.session.commit()
            login_user(new_therapist, remember=True)
            flash('Account Created!', category='success')
            return redirect(url_for('admin.adminDash'))
    return render_template('auth/registerTherapist.html')

@bp.route('/registerPatient', methods=['GET', 'POST'])
def registerPatient():
    therapist_list = User.query.filter_by(is_therapist=True).all()

    if request.method == 'POST':
        first_name = request.form.get('firstname')
        surname = request.form.get('surname')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 chartacter.', category='error')
        elif len(surname) < 2:
            flash('Surname must be greater than 2 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            therapist_choice = request.form.get('therapistList')
            print(therapist_choice)
            new_patient = User(first_name = first_name, surname = surname, email=email, password=generate_password_hash(password1, method='sha256'), is_therapist = False)
            db.session.add(new_patient)
            db.session.commit()
            
            # Association
            new_association = Association(patient_id = new_patient.id, therapist_id = therapist_choice)
            db.session.add(new_association)
            db.session.commit()

            print(new_association.id)
            print(new_association.patient_id)
            print(new_association.therapist_id)

            login_user(new_patient, remember=True)
            flash('Account Created!', category='success')
            return redirect(url_for('main.index'))
    return render_template('auth/register.html', therapist_list = therapist_list)