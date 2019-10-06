"""Initialization of TSkr"""
import atexit
import os
import json
import rpyc
import logging.config
from apscheduler.schedulers import SchedulerAlreadyRunningError
from flask import Flask
from flask_apscheduler import APScheduler
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import MetaData
from config import config

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=naming_convention)
bcrypt = Bcrypt()                                           # flask_bcrypt
login_manager = LoginManager()                              # flask_login
db = SQLAlchemy(metadata=metadata)                          # flask_sqlalchemy
csrf = CSRFProtect()                                        # flask_wtf

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    if os.path.isfile(os.path.join(app.instance_path, "logging.cfg")):
        with app.open_instance_resource("logging.cfg", "r") as json_file:
            logging.config.dictConfig(json.load(json_file))

    config[config_name].init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    app.db = db

    # This will only run in uwsgi prefork mode
    try:
        import uwsgi
        from uwsgidecorators import postfork
        @postfork
        def connect_to_database():
            db.init_app(app)
            app.logger.info("worker #{}: Database Connected".format(uwsgi.worker_id()))
        @postfork
        def connect_to_scheduler():
            core = rpyc.connect("localhost", app.config["CORE_SERVICE_PORT"], config={"allow_public_attrs" : True})
            scheduler = APScheduler(core.root)
            # if uwsgi.worker_id() == 1:
                # scheduler.init_app(app)
                # scheduler.start()
                # app.logger.info("Worker #{}: Trigger Scheduler Start".format(uwsgi.worker_id()))
            # else:
            app.apscheduler = scheduler
            app.logger.info("Worker #{}: Scheduler Connected".format(uwsgi.worker_id()))
    except ImportError:
        app.logger.info("Running without uwsgi")
        db.init_app(app)
        app.logger.info("Database Connected")
        core = rpyc.connect("localhost", app.config["CORE_SERVICE_PORT"], config={"allow_public_attrs" : True})
        scheduler = APScheduler(core.root)
        app.logger.info("Scheduler Connected")

    from .routes.main import main_blueprint
    app.register_blueprint(main_blueprint)

    from .routes.dev import dev_blueprint
    app.register_blueprint(dev_blueprint, url_prefix="/dev")

    from .routes.api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api")

    from .routes.job import job_blueprint
    app.register_blueprint(job_blueprint, url_prefix="/job")

    from .routes.user import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix="/user")

    from .handler import handler
    app.register_blueprint(handler)

    return app
