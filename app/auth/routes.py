from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models import *
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import login_user, login_required, logout_user, current_user

from app.auth import bp
from .forms import RegisterPatientForm, RegisterTherapist

###########################
# REGISTERING FUNCTIONALITY 
###########################

@bp.route('/registerChoice')
def registerChoice():
    return render_template('auth/registerChoice.html')

@bp.route('/registerTherapist', methods=['GET', 'POST'])
def registerTherapist():
    form = RegisterTherapist()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Therapist account already exists. Please register with a different email address.')
        else:
            new_therapist = User(first_name=form.first_name.data, surname=form.surname.data, email=form.email.data, 
            password=generate_password_hash(form.password.data, method="sha256"), is_therapist=True)
            db.session.add(new_therapist)
            db.session.commit()

            login_user(new_therapist, remember=True)
            flash('Therapist account created.', category='success')
            return redirect(url_for('admin.adminDash'))
    return render_template('auth/registerTherapist.html', form=form)

@bp.route('/registerTherapist', methods=['GET', 'POST'])
def registerTherapist():
    form = RegisterTherapist()

    if form.validate_on_submit():
        user = 

@bp.route('/registerPatient', methods=['GET', 'POST'])
def registerPatient():
    form = RegisterPatientForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            flash('Email already exists', category='error')
        else:
            therapist_choice = form.therapist_choice.data
            therapist_choice = User.query.get(therapist_choice)
            print(therapist_choice)
            new_patient = User(first_name=form.first_name.data, surname=form.surname.data, email=form.email.data, 
            password=generate_password_hash(form.password.data, method="sha256"), is_therapist=False)
            db.session.add(new_patient)
            db.session.commit()

            # Create association between patient and therapist
            new_assocation = Association(patient_id = new_patient.id, therapist_id = therapist_choice.id)
            print(new_assocation)
            db.session.add(new_assocation)
            db.session.commit()

            login_user(new_patient, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('main.index'))
    
    return render_template('auth/registerPatient.html', form=form)

###################################
# LOGGING IN/LOGOUT FUNCTIONALITY #
###################################

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