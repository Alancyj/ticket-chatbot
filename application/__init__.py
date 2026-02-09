from flask import Flask
from dotenv import load_dotenv

import os

from .db import db

load_dotenv() # loading env variables

app = Flask(__name__) # initialising flask web app

print("configuring for Database")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

with app.app_context():
    from .table import ChatHistory, Messages, Tickets
    from .seed import seed_tickets_if_empty
    db.init_app(app)
    # db.drop_all()
    db.create_all()
    seed_tickets_if_empty()
    db.session.commit()

print("Setup Database, starting importing for routes.py")

from application import routes # importing routes from routes.py