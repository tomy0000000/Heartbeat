"""Config loader of TSkr"""
import os
import uuid
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Universal Config"""
    DEBUG = False
    TESTING = False
    PREFERRED_URL_SCHEME = "https"
    if "SERVER_NAME" in os.environ:
        SERVER_NAME = os.environ.get("SERVER_NAME")
    if "APPLICATION_ROOT" in os.environ:
        APPLICATION_ROOT = os.environ.get("APPLICATION_ROOT")
    SECRET_KEY = os.environ.get("SECRET_KEY") or str(uuid.uuid4())
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PUSHOVER_TOKEN = os.environ.get("PUSHOVER_TOKEN")

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """Config for local Development"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or \
        "sqlite:///" + os.path.join(basedir, "data-dev.sqlite")

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

class TestingConfig(Config):
    """Config for Testing, Travis CI"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or \
        "sqlite://"
    WTF_CSRF_ENABLED = False

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "sqlite:///" + os.path.join(basedir, "data.sqlite")

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        with app.app_context():
            app.config["SCHEDULER_JOBSTORES"] = {
                "default": {
                    "type": "sqlalchemy",
                    "url": cls.SQLALCHEMY_DATABASE_URI
                }
            }

class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.INFO)
        app.logger.addHandler(syslog_handler)

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "unix": UnixConfig,
    "default": DevelopmentConfig
}
