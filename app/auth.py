from flask import Blueprint, render_template, request

# Auth.py blueprint declaration
auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template('auth/login.html')

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    return render_template('auth/register.html')