from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    with app.app_context():
        print(current_app.name)

    UPLOAD_FOLDER = 'website/static/uploads'

    app.config['SECRET_KEY'] = 'my secret key'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'views.home'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Prediction

    create_database(app)

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')