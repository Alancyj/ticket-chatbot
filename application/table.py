from .db import db
from datetime import datetime, timezone, timedelta

gmt8 = timezone(timedelta(hours=8))

class ChatHistory(db.Model):
    chat_id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(20), nullable= False)

class Messages(db.Model):
    primary_key = db.Column(db.Integer, primary_key=True, autoincrement= True)
    role = db.Column(db.String(10), nullable= False)
    content = db.Column(db.String(1000), nullable= False)
    chat_id = db.Column(db.String(50), nullable= False)

class Tickets(db.Model):
    incident_number = db.Column(db.String(9), primary_key=True)
    incident_title = db.Column(db.String(100), nullable=False)
    incident_description = db.Column(db.String(500), nullable=False)
    incident_resolution = db.Column(db.String(500), nullable=True)
    resolution_team = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), nullable=False)
    status_update_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())
    reported_by = db.Column(db.String(20), nullable=False)
    institution = db.Column(db.String(4), nullable=False)
    institution_name = db.Column(db.String(100), nullable=False)
    reported_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now())
    location = db.Column(db.String(20), nullable=False)
    affected_person_department = db.Column(db.String(20), nullable=False)
    resolution_code = db.Column(db.String(20), nullable=True)
    source = db.Column(db.String(20), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    close_date = db.Column(db.DateTime, nullable=True)