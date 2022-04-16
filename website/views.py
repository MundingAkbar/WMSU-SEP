from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import User, Prediction
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/dashboard')
@login_required
def dashboard():
    unemployed = self_employed_counts = Prediction.query.filter(Prediction.result=='Unemployed').count()
    employed =  self_employed_counts = Prediction.query.filter(Prediction.result=='Employed').count()
    self_employed = self_employed_counts = Prediction.query.filter(Prediction.result=='Self-Employed').count()
    return render_template("admin.html", user_counts = User.query.count(), pred_counts = Prediction.query.count(), employed=employed, unemployed=unemployed, self_employed=10)

@views.route('/delete-user', methods=['POST'])
def delete_user():
    user = json.loads(request.data)
    userId = user['id']
    user = User.query.get(userId)
    if user:
        db.session.delete(user)
        db.session.commit()

    flash('User deleted successfully!', category='success')
    return jsonify({})
