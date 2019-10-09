"""Job Blueprint"""
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from flask import Blueprint, current_app, render_template, redirect, request, session, url_for
from flask_login import login_required
from ..forms import JobForm
job_blueprint = Blueprint("job", __name__)

@job_blueprint.route("/add", methods=["GET", "POST"])
@login_required
def add_job():
    if request.method == "GET":
        tasks = current_app.scheduler.get_tasks()
        form = JobForm(type="add")
        form.func.choices = [(task.split(".")[-1], task) for task in tasks]
        return render_template("job.html", form=form)
    if request.method == "POST":
        form_datas = request.form
        options = {
            "trigger": form_datas["trigger"],
            "args": form_datas["args"],
            "kwargs": form_datas["kwargs"],
            "id": form_datas["id"],
            "name": form_datas["name"],
            "misfire_grace_time": form_datas["misfire_grace_time"],
            "coalesce": bool("coalesce" in form_datas),
            "max_instances": form_datas["max_instances"],
            "next_run_time": form_datas["next_run_time"],
            "executor": form_datas["executor"],
            "replace_existing": bool("replace_existing" in form_datas)
        }
        # response = current_app.scheduler.add_job(
        #     form_datas["func"],
        #     **options,
        #     **trigger_args,
        #     minute=5
        # )
        session["alert"] = form_datas
        session["alert_type"] = "success"
    else:
        session["alert"] = "Something Went Wrong!!!!"
        session["alert_type"] = "warning"
    return redirect(url_for("main.dashboard"))

@job_blueprint.route("/explicit_add")
@login_required
def explicit_add():
    response = current_app.scheduler.add_job(
        "server.task.example:cron_func", #func
        trigger="cron",
        args=None,
        kwargs=None,
        id="test_cron",
        name="test_cron",
        minute=5
    )
    session["alert"] = str(response)
    session["alert_type"] = "success"
    return redirect(url_for("main.dashboard"))

@job_blueprint.route("/<job_id>/modify", methods=["GET", "POST"])
@login_required
def modify(job_id):
    job = current_app.scheduler.get_job(job_id)
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
        return render_template("empty.html", info=form_datas)
    response = "Something Went Wrong!!!!"
    return render_template("empty.html", info=response)
