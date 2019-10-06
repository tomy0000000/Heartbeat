"""Database for SQLAlchemy"""
import codecs
import os
from datetime import datetime
from flask_login import UserMixin
from . import db, bcrypt

def generate_random_id():
    return codecs.encode(os.urandom(16), "hex").decode()

class Users(UserMixin, db.Model):
    __tablename__ = "users"
    username = db.Column(db.String(30), nullable=False, primary_key=True)
    _password_hash = db.Column(db.String(128), nullable=False, unique=False)
    pushover_key = db.Column(db.String(40), unique=False)
    youtube_user_token = db.Column(db.String(40), unique=False)
    @property
    def password(self):
        """Password Property"""
        raise AttributeError("Password is not a readable attribute")
    @password.setter
    def password(self, password):
        if len(password) < 6:
            raise ValueError("Password must be longer than 6 characters")
        if len(password) > 30:
            raise ValueError("Password must be shorter than 30 characters")
        self._password_hash = bcrypt.generate_password_hash(password)
    def __init__(self, username, password, pushover_key=None, youtube_user_token=None):
        self.username = username
        self.password = password
        self.pushover_key = pushover_key
        self.youtube_user_token = youtube_user_token
    def __repr__(self):
        return "<users %r>" %self.username
    def is_authenticated(self):
        # TODO
        return True
    def get_id(self):
        return self.username
    def check_password(self, password):
        """Return True if provided password is valid to login"""
        return bcrypt.check_password_hash(self._password_hash, password)

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

class APShedulerJobs(db.Model):
    """A Dummy Model for Flask Migrate"""
    __tablename__ = "apscheduler_jobs"
    id = db.Column(db.String(32), nullable=False, primary_key=True)
    next_run_time = db.Column(db.Float(64), index=True)
    job_state = db.Column(db.LargeBinary, nullable=False)
