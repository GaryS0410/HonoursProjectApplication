from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

# Auth.py blueprint declaration
auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
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
                return redirect(url_for('views.index'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('Account doesn\'t exist', category='error')
            print("no account")

    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods = ['GET', 'POST'])
def register():
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
            flash('Email too must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be grater than 1 characters.', category='error')
        elif len(surname) < 2:
            flash('Surname must be greater than 2 characters', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', categor='error') 
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else: 
            new_user = User(first_name = first_name, surname = surname, email=email, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account Created!', category='success')
            return redirect(url_for('views.index'))

    return render_template('auth/register.html')