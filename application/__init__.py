from flask import Flask
from dotenv import load_dotenv

import os

from .db import db

load_dotenv() # loading env variables

app = Flask(__name__) # initialising flask web app

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

with app.app_context():
    from .table import ChatHistory, Messages
    db.init_app(app)
    db.drop_all()
    db.create_all()
    db.session.commit()

from application import routes # importing routes from routes.py