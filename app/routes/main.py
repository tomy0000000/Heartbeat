"""Main Blueprint"""
from flask import Blueprint, current_app, render_template
from flask_login import login_required
main_blueprint = Blueprint("main", __name__)

@main_blueprint.route("/")
@login_required
def dashboard():
    jobs = current_app.apscheduler.get_jobs()
    return render_template("dashboard.html", jobs=jobs)

@main_blueprint.route("/history")
def history():
    return render_template("empty.html")
