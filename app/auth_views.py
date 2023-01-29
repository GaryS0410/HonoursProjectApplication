from app import app
from flask import Flask, render_template, request, Response, jsonify, make_response

@app.route('/login')
def login():
    return render_template('auth/login.html')

@app.route('/register')
def register():
    return render_template('auth/register.html')