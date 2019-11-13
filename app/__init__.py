# app/__init__.py

from flask import Flask
from flask_googlemaps import GoogleMaps
import os
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
if GOOGLE_API_KEY:
    logger.debug('Loaded Google API Key %s', GOOGLE_API_KEY)
else:
    logger.error('No environment variable set for Google API key - export GOOGLE_API_KEY=XXX')


# Initialize the app
app = Flask(__name__, instance_relative_config=True)

# Load the views
from app import controller, model
#from app import views, controller, model

# Load the config file
app.config.from_object('config')

# todo: pass api key from config file
GoogleMaps(app, key=GOOGLE_API_KEY)