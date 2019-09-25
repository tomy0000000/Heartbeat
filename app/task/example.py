"""Functions for Example Tasks"""
import logging
import uuid
from datetime import datetime, timedelta
from flask import current_app

def date_func(session_id):
    logger = logging.getLogger(name="testing_date")
    logger.warning(session_id)
    logger.info(datetime.now())
    fire_datetime = datetime.now() + timedelta(minutes=5)
    job_response = current_app.apscheduler.add_job(
        id="date_job",
        func=date_func,
        args=[str(uuid.uuid4())],
        trigger="date",
        run_date=fire_datetime)
    logger.debug(job_response)

def interval_func(session_id):
    logger = logging.getLogger(name="testing_interval")
    logger.warning(session_id)
    logger.info(datetime.now())

def cron_func(session_id):
    logger = logging.getLogger(name="testing_cron")
    logger.warning(session_id)
    logger.info(datetime.now())
