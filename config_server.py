import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

SERVER_PORT = 4792
PROTOCOL_CONFIG = {"allow_public_attrs": True}
SERVER_SSL_KEYFILE = os.environ.get("SERVER_SSL_KEYFILE") or None
SERVER_SSL_CERTFILE = os.environ.get("SERVER_SSL_CERTFILE") or None

SCHEDULER_CONFIG = {
    "jobstores": {
        "default": {
            "type": "sqlalchemy",
            "url": os.environ.get("DATABASE_URL") or \
                "sqlite:///" + os.path.join(basedir, "data.sqlite")
        }
    },
    "executors": {

    },
    "job_defaults": {

    },
    # "timezone": ""
}

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
        "core_trfh": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "log/core.log",
            "when": "D",
            "interval": 1,
            "backupCount": 7
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["console", "core_trfh"],
            "level": "INFO",
            "propagate": False
        },
        # "Heartbeat.core": {
        #     "handlers": ["core_trfh"],
        #     "level": "INFO"
        # },
        # "__main__": {  # if __name__ == "__main__"
        #     "handlers": ["default"],
        #     "level": "DEBUG",
        #     "propagate": False
        # },
    }
}
