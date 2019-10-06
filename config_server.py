import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
config = {
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
