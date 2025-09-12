from flask import Flask
from dotenv import load_dotenv

load_dotenv() # loading env variables

app = Flask(__name__) # initialising flask web app

from application import routes # importing routes from routes.py