"""dev Blueprint"""
import os
import sys
import uwsgi
import signal
from flask import Blueprint, current_app, request, render_template, url_for
from ..helper import send_notification
dev_blueprint = Blueprint("dev", __name__)

@dev_blueprint.route("/api/push", methods=["GET", "POST"])
def api_push():
    if request.method == "GET":
        return render_template("pushover_push.html")
    if request.method == "POST":
        form_datas = request.form
        response = send_notification("Test", form_datas["message"], title=form_datas["title"])
        return render_template("empty.html", content=response)
    response = "Something Went Wrong!!!!"
    return render_template("empty.html", content=response)

@dev_blueprint.route("/sitemap")
def sitemap():
    links = []
    for rule in current_app.url_map.iter_rules():
        query = {arg: "[{0}]".format(arg) for arg in rule.arguments}
        url = url_for(rule.endpoint, **query)
        links.append((url, rule.endpoint))
    links.sort(key=lambda x: x[1])
    return render_template("sitemap.html", links=links)

@dev_blueprint.route("/empty")
def empty():
    return render_template("empty.html")

@dev_blueprint.route("/dict_sys")
def dict_sys():
    target_dict = sys.__dict__
    return render_template("empty.html", content=target_dict)

@dev_blueprint.route("/dict_flask")
def dict_flask():
    target_dict = current_app.__dict__
    return render_template("empty.html", content=target_dict)

@dev_blueprint.route("/uwsgi_workers")
def uwsgi_workers():
    target_dict = uwsgi.workers()
    return render_template("empty.html", content=target_dict)

@dev_blueprint.route("/uwsgi_applist")
def uwsgi_applist():
    target_dict = uwsgi.started_on
    return render_template("empty.html", content=target_dict)

@dev_blueprint.route("/uwsgi_workers_reload")
def uwsgi_workers_reload():
    os.kill(uwsgi.masterpid(), signal.SIGHUP)
    response = "Workers reloaded"
    return render_template("empty.html", content=response)

@dev_blueprint.route("/uwsgi_worker_reload/<worker_id>")
def uwsgi_worker_reload(worker_id):
    pid = None
    for worker in uwsgi.workers():
        if worker["id"] == int(worker_id):
            pid = worker["pid"]
    if not pid:
        response = "Worker {} doesn't exists".format(worker_id)
    else:
        os.kill(pid, signal.SIGINT)
        response = "Worker {} reloaded".format(worker_id)
    return render_template("empty.html", content=response)
