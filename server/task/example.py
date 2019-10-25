"""Functions for Example Tasks"""
import logging
import uuid
from datetime import datetime, timedelta
from flask import current_app

__all__ = ["date_func", "interval_func", "cron_func"]

def date_func():
    logger = logging.getLogger(name="testing_date")
    logger.info(datetime.now())
    fire_datetime = datetime.now() + timedelta(minutes=5)
    job_response = current_app.apscheduler.add_job(
        id="test_date",
        name="test_date",
        func=date_func,
        trigger="date",
        run_date=fire_datetime)
    logger.debug(job_response)

def interval_func():
    logger = logging.getLogger(name="testing_interval")
    logger.info(datetime.now())

def cron_func():
    logger = logging.getLogger(name="testing_cron")
    logger.info(datetime.now())
