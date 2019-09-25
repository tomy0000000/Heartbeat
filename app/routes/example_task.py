"""Blueprint for adding example Task"""
import uuid
from datetime import datetime, timedelta
from flask import Blueprint, current_app, render_template
from ..task.example import date_func, interval_func, cron_func
example_task_blueprint = Blueprint("example_task", __name__)

@example_task_blueprint.route("/add-test-date")
def add_test_date_job():
    fire_datetime = datetime.now() + timedelta(minutes=5)
    job_response = current_app.apscheduler.add_job(
        id="date_job",
        func=date_func,
        args=[str(uuid.uuid4())],
        trigger="date",
        run_date=fire_datetime)
    return render_template("empty.html", content=job_response)

@example_task_blueprint.route("/add-test-interval")
def add_test_interval_job():
    job_response = current_app.apscheduler.add_job(
        id="interval_job",
        func=interval_func,
        args=[str(uuid.uuid4())],
        trigger="interval",
        minutes=5)
    return render_template("empty.html", content=job_response)

@example_task_blueprint.route("/add-test-cron")
def add_test_cron_job():
    job_response = current_app.apscheduler.add_job(
        id="cron_job",
        func=cron_func,
        args=[str(uuid.uuid4())],
        trigger="cron",
        minute=5)
    return render_template("empty.html", content=job_response)
