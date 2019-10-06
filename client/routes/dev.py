"""dev Blueprint"""
import os
import sys
import signal
from flask import Blueprint, current_app, request, render_template, url_for
from flask_login import login_required
dev_blueprint = Blueprint("dev", __name__)

@dev_blueprint.route("/sitemap")
@login_required
def sitemap():
    links = []
    for rule in current_app.url_map.iter_rules():
        query = {arg: "[{0}]".format(arg) for arg in rule.arguments}
        url = url_for(rule.endpoint, **query)
        links.append((url, rule.endpoint))
    links.sort(key=lambda x: x[1])
    return render_template("sitemap.html", links=links)

@dev_blueprint.route("/empty")
@login_required
def empty():
    return render_template("empty.html")

@dev_blueprint.route("/dict_sys")
@login_required
def dict_sys():
    target_dict = sys.__dict__
    return render_template("empty.html", info=target_dict)

@dev_blueprint.route("/dict_flask")
@login_required
def dict_flask():
    target_dict = current_app.__dict__
    return render_template("empty.html", info=target_dict)

@dev_blueprint.route("/dict_scheduler")
@login_required
def dict_scheduler():
    target_dict = current_app.apscheduler.__dict__
    return render_template("empty.html", info=target_dict)

@dev_blueprint.route("/uwsgi_workers")
@login_required
def uwsgi_workers():
    import uwsgi
    target_dict = uwsgi.workers()
    return render_template("empty.html", info=target_dict)

@dev_blueprint.route("/uwsgi_applist")
@login_required
def uwsgi_applist():
    import uwsgi
    target_dict = uwsgi.started_on
    return render_template("empty.html", info=target_dict)

@dev_blueprint.route("/uwsgi_workers_reload")
@login_required
def uwsgi_workers_reload():
    import uwsgi
    os.kill(uwsgi.masterpid(), signal.SIGHUP)
    response = "Workers reloaded"
    return render_template("empty.html", info=response)

@dev_blueprint.route("/uwsgi_worker_reload/<worker_id>")
@login_required
def uwsgi_worker_reload(worker_id):
    import uwsgi
    pid = None
    for worker in uwsgi.workers():
        if worker["id"] == int(worker_id):
            pid = worker["pid"]
    if not pid:
        response = "Worker {} doesn't exists".format(worker_id)
    else:
        os.kill(pid, signal.SIGINT)
        response = "Worker {} reloaded".format(worker_id)
    return render_template("empty.html", info=response)
