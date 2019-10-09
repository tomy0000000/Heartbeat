"""Config loader of Heartbeat Client"""
import os
import uuid
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Universal Config"""
    DEBUG = False
    TESTING = False
    PREFERRED_URL_SCHEME = "https"
    SERVER_NAME = os.environ.get("CLIENT_SERVER_NAME") or None
    APPLICATION_ROOT = os.environ.get("CLIENT_APPLICATION_ROOT") or "/"
    SECRET_KEY = os.environ.get("SECRET_KEY") or str(uuid.uuid4())
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORE_SERVICE_PORT = 4792
    CLIENT_SSL_KEYFILE = os.environ.get("CLIENT_SSL_KEYFILE") or None
    CLIENT_SSL_CERTFILE = os.environ.get("CLIENT_SSL_CERTFILE") or None
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
    """Config for Production Deployment"""
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "sqlite:///" + os.path.join(basedir, "data.sqlite")

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

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
