from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    course = db.Column(db.Integer)
    epic = db.Column(db.Integer)
    academic_awards = db.Column(db.Integer)
    num_trainings = db.Column(db.Float)
    s1 = db.Column(db.Integer)
    s2 = db.Column(db.Integer)
    s3 = db.Column(db.Integer)
    s4 = db.Column(db.Integer)
    s5 = db.Column(db.Integer)
    s6 = db.Column(db.Integer)
    s7 = db.Column(db.Integer)
    s8 = db.Column(db.Integer)
    s9 = db.Column(db.Integer)
    s10 = db.Column(db.Integer)
    result = db.Column(db.String(150))
    user_id = db.Column(db.String(150), db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    middle_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    role = db.Column(db.String(150))
    image = db.Column(db.Text)
    password_changed = db.Column(db.Boolean, default=False)
    filename = db.Column(db.Text, default="no-image.png")
    mimetype = db.Column(db.Text)
    prediction = db.relationship('Prediction')