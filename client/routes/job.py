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
    alert = session.pop("alert", None)
    alert_type = session.pop("alert_type", None)
    tasks = current_app.scheduler.get_tasks()
    form = JobForm(type="add")
    form.base_args.func.choices = [("", "")]+[(task, task.split(".")[-1]) for task in tasks]
    if request.method == "POST":
        if form.validate_on_submit():
            current_app.logger.info("Form Validated")
            valid_args = ["args", "kwargs", "coalesce", "trigger", "executor", "misfire_grace_time", "max_instances", "next_run_time", "replace_existing"]
            valid_trigger = ["cron", "date", "interval"]
            valid_trigger_args = {
                "cron": ["day", "end_date", "hour", "jitter", "minute", "month", "second", "start_date", "timezone", "week", "year"],
                "date": ["run_date", "timezone"],
                "interval": ["weeks", "days", "hours", "minutes", "seconds", "start_date", "end_date", "timezone", "jitter"]
            }

            options = {
                "id": form.base_args.job_id.data,
                "name": form.base_args.job_name.data
            }
            trigger_args = {}
            trigger = form.base_args.trigger.data
            if trigger not in valid_trigger:
                raise ValueError("Invalid Trigger")
            for arg, val in form.data["base_args"].items():
                if arg in valid_args and val:
                    options[arg] = val
            for arg, val in form.data["{}_trigger_args".format(trigger)].items():
                if arg in valid_trigger_args[trigger] and val:
                    trigger_args[arg] = val

            try:
                response = current_app.scheduler.add_job(
                    form.base_args.func.data,
                    **options,
                    **trigger_args,
                )
                session["alert"] = {"func": form.base_args.func.data, **options, **trigger_args}
                session["alert_type"] = "success"
                return redirect(url_for("main.dashboard"))
            except Exception as error:
                alert = "{}: {}".format(type(error).__name__, error.args)
                alert_type = "danger"
    return render_template("job.html",
                           form=form,
                           alert=alert,
                           alert_type=alert_type)

@job_blueprint.route("/<job_id>/modify", methods=["GET", "POST"])
@login_required
def modify(job_id):
    alert = session.pop("alert", None)
    alert_type = session.pop("alert_type", None)
    tasks = current_app.scheduler.get_tasks()
    form = JobForm(type="modify")
    form.base_args.func.choices = [("", "")]+[(task, task.split(".")[-1]) for task in tasks]
    job = current_app.scheduler.get_job(job_id)
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                # response = job.modify(**options, **trigger_args)
                # session["alert"] = {**options, **trigger_args}
                # session["alert_type"] = "success"
                return redirect(url_for("main.dashboard"))
            except Exception as error:
                alert = "{}: {}".format(type(error).__name__, error.args)
                alert_type = "danger"
    if request.method == "GET":
        form.base_args.job_id.data = job.id
        form.base_args.job_name.data = job.name
        form.base_args.func.data = job.func #Fixme
        form.base_args.trigger.data = type(job.trigger).__name__.split(".")[2]
        # job.next_run_time = job.next_run_time.strftime("%Y-%m-%dT%H:%m")
    return render_template("job.html",
                           form=form,
                           job=job,
                           alert=alert,
                           alert_type=alert_type)

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
