"""Blueprint for TSkr"""
import codecs
import logging
import os
from datetime import datetime, timedelta
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from flask import Blueprint, redirect, request, render_template, url_for
from flask_login import current_user, login_user, logout_user, login_required
from .. import login_manager, scheduler
from ..forms import JobForm, LoginForm
from ..helper import send_notification
from ..models import Users
main_blueprint = Blueprint("main", __name__)

#     #######
#     #       #    # #    #  ####   ####
#     #       #    # ##   # #    # #
#     #####   #    # # #  # #       ####
#     #       #    # #  # # #           #
#     #       #    # #   ## #    # #    #
#     #        ####  #    #  ####   ####

def generate_random_id():
    return codecs.encode(os.urandom(16), "hex").decode()

def date_func(session_id):
    logger = logging.getLogger(name="testing_date")
    logger.warning(session_id)
    logger.info(datetime.now())
    fire_datetime = datetime.now() + timedelta(minutes=5)
    job_response = scheduler.add_job(
        id="date_job",
        func=date_func,
        args=[generate_random_id()],
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


#     #     #
#     #     #   ##   #    # #####  #      ###### #####
#     #     #  #  #  ##   # #    # #      #      #    #
#     ####### #    # # #  # #    # #      #####  #    #
#     #     # ###### #  # # #    # #      #      #####
#     #     # #    # #   ## #    # #      #      #   #
#     #     # #    # #    # #####  ###### ###### #    #

@main_blueprint.errorhandler(401)
def page_unauthorized(error):
    """A Page Not Found Handler"""
    send_notification("401 Alert", str(datetime.now()),
                      title="TSkr received an 401 Error!!")
    return render_template("error.html", error=error), 401

@main_blueprint.errorhandler(404)
def page_not_found(error):
    """A Page Not Found Handler"""
    send_notification("404 Alert", str(datetime.now()),
                      title="TSkr received an 404 Error!!")
    return render_template("error.html", error=error), 404

#     #       #######  #####  ### #     #
#     #       #     # #     #  #  ##    #
#     #       #     # #        #  # #   #
#     #       #     # #  ####  #  #  #  #
#     #       #     # #     #  #  #   # #
#     #       #     # #     #  #  #    ##
#     ####### #######  #####  ### #     #

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

#     ######
#     #     #  ####  #    # ##### ######  ####
#     #     # #    # #    #   #   #      #
#     ######  #    # #    #   #   #####   ####
#     #   #   #    # #    #   #   #           #
#     #    #  #    # #    #   #   #      #    #
#     #     #  ####   ####    #   ######  ####

@main_blueprint.route("/")
def dashboard():
    jobs = scheduler.get_jobs()
    return render_template("dashboard.html", jobs=jobs)

@main_blueprint.route("/add-test-date")
def add_test_date_job():
    fire_datetime = datetime.now() + timedelta(minutes=5)
    job_response = scheduler.add_job(
        id="date_job",
        func=date_func,
        args=[generate_random_id()],
        trigger="date",
        run_date=fire_datetime)
    return render_template("empty.html", content=job_response)

@main_blueprint.route("/add-test-interval")
def add_test_interval_job():
    job_response = scheduler.add_job(
        id="interval_job",
        func=interval_func,
        args=[generate_random_id()],
        trigger="interval",
        minutes=5)
    return render_template("empty.html", content=job_response)

@main_blueprint.route("/add-test-cron")
def add_test_cron_job():
    job_response = scheduler.add_job(
        id="cron_job",
        func=cron_func,
        args=[generate_random_id()],
        trigger="cron",
        minute=5)
    return render_template("empty.html", content=job_response)

@main_blueprint.route("/add", methods=["GET", "POST"])
def add_job():
    if request.method == "GET":
        form = JobForm(type="add")
        return render_template("job.html", form=form)
    if request.method == "POST":
        form_datas = request.form
        # response = scheduler.add_job(**kwargs)
        return render_template("empty.html", content=form_datas)
    response = "Something Went Wrong!!!!"
    return render_template("empty.html", content=response)

@main_blueprint.route("/<job_id>/run")
def run_job(job_id):
    response = scheduler.get_job(job_id).func(manual=True)
    return render_template("empty.html", content=response)

@main_blueprint.route("/<job_id>/pause")
def pause_job(job_id):
    response = scheduler.get_job(job_id).pause()
    return render_template("empty.html", content=response)

@main_blueprint.route("/<job_id>/resume")
def resume_job(job_id):
    response = scheduler.get_job(job_id).resume()
    return render_template("empty.html", content=response)

@main_blueprint.route("/<job_id>/modify", methods=["GET", "POST"])
def modify_job(job_id):
    job = scheduler.get_job(job_id)
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

@main_blueprint.route("/<job_id>/remove")
def delete_job(job_id):
    scheduler.get_job(job_id).remove()
    return render_template("empty.html", content="Job #"+job_id+" Removed")

@main_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("secret"))
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user is not None and user.valid_password(form.password.data):
            login_user(user)
            return redirect(url_for("secret"))
        error = "Invalid username or password."
    return render_template("login.html", form=form, error=error)

@main_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@main_blueprint.route("/secret")
@login_required
def secret():
    return render_template("empty.html",
                           content="Welcome, {}".format(current_user.username))

@main_blueprint.route("/history")
def history():
    return render_template("empty.html")
