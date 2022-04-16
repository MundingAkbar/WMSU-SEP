from re import A
from flask import Blueprint,render_template,request,flash, redirect , url_for, current_app
from .models import User, Prediction
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from . import models
from flask_login import login_user, login_required, logout_user, current_user
import os
from os import path
import urllib.request
from werkzeug.utils import secure_filename
# imports for prediction
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.metrics import accuracy_score
import pandas as pd
import pickle

auth = Blueprint('auth', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route('/', methods=['GET', 'POST'])
def login():   
    if request.method == "POST":
        email = request.form.get('user_id')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                if user.role == 'admin':
                    login_user(user, remember=True)
                    return redirect(url_for('views.dashboard'))
                else:
                    login_user(user, remember=True)
                    return redirect(url_for("auth.user"))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('User id doesnt exist.', category='error')

    return render_template('home.html')

@auth.route('/manage_students', methods=['GET', 'POST'])
# @login_required
def manage_students():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        image = request.files['image']

        user = User.query.filter_by(email=str(email)).first()

        if user:
            flash('This user ID already exist.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character!', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character!', category='error')
        elif len(password) < 7:
            flash('Password must be greater than 6 character!', category='error')
        elif len(password) < 7:
          flash('Student ID must be greater than 6 character!', category='error')
        else:
            if image:
                if allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    mimetype = image.mimetype
                    image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

                    new_user = User(email=email,first_name=first_name,middle_name=middle_name,last_name=last_name,password=generate_password_hash(password, method='sha256'),role='student',image=image.read(),mimetype=mimetype,filename=filename)
                    db.session.add(new_user)
                    db.session.commit()
                    flash('New student with profile image account added successfully!', category='success')
                else:
                    flash('The image extension is not supported, please choose the right image file!', category='error')
            else:
                new_user = User(email=email,first_name=first_name,middle_name=middle_name,last_name=last_name,password=generate_password_hash(password, method='sha256'),role='student')
                db.session.add(new_user)
                db.session.commit()
                flash('New student account added successfully!', category='success')

    return render_template("manage_students.html", users = User.query.all())

@auth.route('/user', methods=['GET','POST'])
@login_required
def user():
    if 'new_password' in request.form:
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        if new_password != confirm_password:
            flash('Please make sure to make the same and confirm your password', category='error')
        elif len(new_password) < 7 or len(confirm_password) < 7:
            flash('Password must be greater than or equal to 7', category='error')
        else:
            current_user.password = generate_password_hash(new_password, method='sha256')
            current_user.password_changed = True
            db.session.commit()
            flash('Your password has been changed successfully!', category='success')
    else:
        pred = Prediction.query.filter_by(user_id=current_user.id).first()
        if pred:
            return render_template('user.html', user=current_user, result = pred.result)
    
        if request.method == 'POST':
            age = request.form.get('age')
            epic = request.form['epic']
            academic_awards = request.form.get('academic_awards')
            course = request.form.get('course')
            num_trainings = request.form.get('num_trainings')
            s1 = request.form.get('s1')
            s2 = request.form.get('s2')
            s3 = request.form.get('s3')
            s4 = request.form.get('s4')
            s5 = request.form.get('s5')
            s6 = request.form.get('s6')
            s7 = request.form.get('s7')
            s8 = request.form.get('s8')
            s9 = request.form.get('s9')
            s10 = request.form.get('s10')

            #fetching the saved model
            with open('website/data_set','rb') as f:
                model = pickle.load(f)
            # make prediction
            prediction = model.predict([ [age, s1, s2, s3, s4, s5, s6, s7, s8, num_trainings , s9, s10, academic_awards, epic, course] ])

            #saving prediction to database
            new_prediction = Prediction(age=age, course=course, academic_awards=academic_awards, epic=epic, num_trainings=num_trainings, s1=s1, s2=s2, s3=s3, s4=s4, s5=s5, s6=s6, s7=s7, s8=s8, result=prediction[0],user_id=current_user.id)
            db.session.add(new_prediction)
            db.session.commit()
            flash('prediction submited!', category='success')
            return render_template('user.html', user=current_user, result=prediction[0])

    return render_template('user.html', user=current_user)

# @auth.route('/display/<filename>')
# def display_image(filename):
#     return redirect(url_for('static',filename='uploads'/+filename))
@auth.route('/profile')
def profile():
    return render_template('profile.html')

@auth.route('/update')
def update():
    return '<p>hello</p>'

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('/add_student')
def add_student():
    return "<p>Student added</p>"
