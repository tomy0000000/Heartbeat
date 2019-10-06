"""API Blueprint"""
from flask import Blueprint, current_app, jsonify
api_blueprint = Blueprint("api", __name__)

@api_blueprint.route("/tasks")
def get_tasks():
    tasks = current_app.apscheduler.scheduler.get_tasks()
    return jsonify(list(tasks))

@api_blueprint.route("/<job_id>/run")
def job_run(job_id):
    response = current_app.apscheduler.get_job(job_id).func(manual=True)
    return jsonify(response)

@api_blueprint.route("/<job_id>/pause")
def job_pause(job_id):
    response = current_app.apscheduler.get_job(job_id).pause()
    return jsonify(response)

@api_blueprint.route("/<job_id>/resume")
def job_resume(job_id):
    response = current_app.apscheduler.get_job(job_id).resume()
    return jsonify(response)
