"""
The Flask application package.
"""

import logging
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session

# Initialize the Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Set up logging
app.logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
app.logger.addHandler(stream_handler)

# Initialize extensions
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'
Session(app)

# Import views after initializing the app and extensions
import FlaskWebProject.views
