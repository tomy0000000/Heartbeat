"""Database for SQLAlchemy"""
import codecs
import os
from datetime import datetime
from flask_login import UserMixin
from . import db

def generate_random_id():
    return codecs.encode(os.urandom(16), "hex").decode()

class Users(UserMixin, db.Model):
    __tablename__ = "users"
    username = db.Column(db.String(30), nullable=False, primary_key=True)
    password = db.Column(db.String(30), nullable=False, server_default=None, unique=False)
    pushover_key = db.Column(db.String(40), nullable=False, server_default=None, unique=False)
    youtube_user_token = db.Column(db.String(40), nullable=False, server_default=None, unique=False)
    def __init__(self, username, password, pushover_key=None, youtube_user_token=None):
        self.username = username
        self.password = password
        self.pushover_key = pushover_key
        self.youtube_user_token = youtube_user_token
    def __repr__(self):
        return "<users %r>" %self.username
    def get_id(self):
        return self.username
    def valid_password(self, password):
        return self.password == password

class Notification(db.Model):
    """
    id              a unique id for identification
    initiator       which function/action fired this notification
    send_datetime   dt when this notification fired
    message         content of the notification
    response        recieved resopnse from Pushover Server
    """
    __tablename__ = "notification"
    id = db.Column(db.String(32), nullable=False, primary_key=True)
    initiator = db.Column(db.String(15), nullable=False, server_default=None, unique=False)
    sent_datetime = db.Column(db.DateTime, nullable=False, server_default=None, unique=False)
    message = db.Column(db.String(2000), nullable=False, server_default=None, unique=False)
    kwargs = db.Column(db.String(10000), nullable=False, server_default=None, unique=False)
    response = db.Column(db.String(150), nullable=False, server_default=None, unique=False)
    def __init__(self, initiator, message, kwargs, response, sent_datetime=datetime.now()):
        self.id = generate_random_id()
        self.initiator = initiator
        self.sent_datetime = sent_datetime
        self.message = message
        self.kwargs = kwargs
        self.response = response
    def __repr__(self):
        return "<notification %r>" %self.id
