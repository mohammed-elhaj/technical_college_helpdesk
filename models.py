from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from init_db import db, User, Request, Message

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    requests = db.relationship('Request', backref='user', lazy=True)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    location_type = db.Column(db.String(20), nullable=False)
    location_number = db.Column(db.String(20), nullable=False)
    problem_type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(200))
    status = db.Column(db.String(20), default='قيد المعالجة')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship('Message', backref='request', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
