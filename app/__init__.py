"""Initialization of TSkr"""
import atexit
import os
import json
import logging.config
from flask import Flask
from flask_apscheduler import APScheduler
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from config import config

import uwsgi
from uwsgidecorators import postfork

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=naming_convention)
scheduler = APScheduler()                                   # flask_apscheduler
login_manager = LoginManager()                              # flask_login
db = SQLAlchemy(metadata=metadata)                          # flask_sqlalchemy

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    if os.path.isfile(os.path.join(app.instance_path, "logging.cfg")):
        with app.open_instance_resource("logging.cfg", "r") as json_file:
            logging.config.dictConfig(json.load(json_file))
    login_manager.init_app(app)
    scheduler.init_app(app)

    # This will only run in prefork mode
    @postfork
    def worker_says_hello():
        print("Hello from {}".format(uwsgi.worker_id()))

    @postfork
    def connect_to_database():
        db.init_app(app)
        print("worker #{}: database connected".format(uwsgi.worker_id()))

    @postfork
    def start_one_scheduler():
        if uwsgi.worker_id() == 1:
            scheduler.start()
            print("Worker #{}: Scheduler Start".format(uwsgi.worker_id()))
        else:
            print("Worker #{}: Scheduler Init".format(uwsgi.worker_id()))

    from .routes.main import main_blueprint
    app.register_blueprint(main_blueprint)
    from .routes.dev import dev_blueprint
    app.register_blueprint(dev_blueprint)
    return app
