from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database.db')
DB_URI = f"sqlite:///{DB_PATH}"

def create_app():
      app = Flask(__name__)
      app.config['SECRET_KEY'] = 'My Super Secret Key'

      app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
      db.init_app(app)

      from .views import views
      from .auth import auth

      app.register_blueprint(views, url_prefix='/')
      app.register_blueprint(auth, url_prefix='/')

      from .models import Note, User

      # Create Database Tables
      with app.app_context():
         db.create_all()

      # Where should the user go when not logged in
      login_manager = LoginManager()
      login_manager.login_view = 'auth.login'
      login_manager.init_app(app)

      # Telling flask how we load a user
      # We are looking for User model and we are going to reference by their id
      @login_manager.user_loader
      def load_user(id):
         return User.query.get(int(id))

      return app
