"""Main Blueprint"""
from flask import Blueprint, current_app, render_template, session
from flask_login import login_required
main_blueprint = Blueprint("main", __name__)

@main_blueprint.route("/")
@login_required
def dashboard():
    alert = session.pop("alert", None)
    alert_type = session.pop("alert_type", None)
    jobs = current_app.scheduler.get_jobs()
    return render_template("dashboard.html",
                           jobs=jobs,
                           alert=alert,
                           alert_type=alert_type)

@main_blueprint.route("/history")
@login_required
def history():
    return render_template("empty.html")
