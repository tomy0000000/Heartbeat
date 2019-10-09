"""Initialize Client App"""
import os
import json
import logging.config
import rpyc
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import MetaData
from config_client import config

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

def init_database(app, db, worker_id=None):
    db.init_app(app)
    app.logger.info(
        "{}Database Connected".format(
            "worker #{}: ".format(worker_id) if worker_id else ""
        )
    )
    app.db = db

def init_scheduler(app, worker_id=None):
    connected = False
    if app.config["CLIENT_SSL_KEYFILE"] and app.config["CLIENT_SSL_CERTFILE"]:
        key_path = os.path.join(app.instance_path, app.config["CLIENT_SSL_KEYFILE"])
        cert_path = os.path.join(app.instance_path, app.config["CLIENT_SSL_CERTFILE"])
        if os.path.exists(key_path) and os.path.exists(cert_path):
            core = rpyc.ssl_connect(
                "localhost",
                app.config["CORE_SERVICE_PORT"],
                config={"allow_public_attrs" : True},
                keyfile=key_path,
                certfile=cert_path
            )
            connected = True
    if not connected:
        core = rpyc.connect(
            "localhost",
            app.config["CORE_SERVICE_PORT"],
            config={"allow_public_attrs" : True}
        )
    app.logger.info(
        "{}Scheduler Connected with{} SSL".format(
            "worker #{}: ".format(worker_id) if worker_id else "",
            "" if connected else "out"
        )
    )
    app.scheduler = core.root

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

    # Make sure connection are established per-worker
    try:
        import uwsgi
        from uwsgidecorators import postfork
        @postfork
        def establish_connection():
            init_database(app, db, uwsgi.worker_id())
            init_scheduler(app, uwsgi.worker_id())
    except ImportError:
        app.logger.info("Running without uwsgi")
        init_database(app, db)
        init_scheduler(app)

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
