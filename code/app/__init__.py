# app/__init__.py

from flask import Flask

# Initialize the app
app = Flask(__name__, instance_relative_config=True)

# Load the views
from app import controller, model
#from app import views, controller, model

# Load the config file
app.config.from_object('config')
