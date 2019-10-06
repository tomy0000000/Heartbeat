"""Job Blueprint"""
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from flask import Blueprint, current_app, render_template, request
from ..forms import JobForm
job_blueprint = Blueprint("job", __name__)

@job_blueprint.route("/add", methods=["GET", "POST"])
def add_job():
    if request.method == "GET":
        form = JobForm(type="add")
        return render_template("job.html", form=form)
    if request.method == "POST":
        form_datas = request.form
        # response = current_app.apscheduler.add_job(**kwargs)
        return render_template("empty.html", content=form_datas)
    response = "Something Went Wrong!!!!"
    return render_template("empty.html", content=response)

@job_blueprint.route("/<job_id>/modify", methods=["GET", "POST"])
def modify_job(job_id):
    job = current_app.apscheduler.get_job(job_id)
    if request.method == "GET":
        if isinstance(job.trigger, CronTrigger):
            trigger_value = "cron"
        elif isinstance(job.trigger, DateTrigger):
            trigger_value = "date"
        elif isinstance(job.trigger, IntervalTrigger):
            trigger_value = "interval"
        else:
            trigger_value = ""
        form = JobForm(trigger=trigger_value, type="modify")
        job.next_run_time = job.next_run_time.strftime("%Y-%m-%dT%H:%m")
        return render_template("job.html", form=form, job=job)
    if request.method == "POST":
        form_datas = request.form
        # response = job.modify(**changes)
        return render_template("empty.html", content=form_datas)
    response = "Something Went Wrong!!!!"
    return render_template("empty.html", content=response)

@job_blueprint.route("/<job_id>/remove")
def delete_job(job_id):
    current_app.apscheduler.get_job(job_id).remove()
    return render_template("empty.html", content="Job #"+job_id+" Removed")
