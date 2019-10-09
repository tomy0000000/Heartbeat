"""API Blueprint"""
from flask import Blueprint, current_app, jsonify
api_blueprint = Blueprint("api", __name__)

@api_blueprint.route("/tasks")
def get_tasks():
    tasks = current_app.scheduler.get_tasks()
    return jsonify(list(tasks))

@api_blueprint.route("/<job_id>/run")
def job_run(job_id):
    response = current_app.scheduler.get_job(job_id).func(manual=True)
    return jsonify(str(response))

@api_blueprint.route("/<job_id>/pause")
def job_pause(job_id):
    response = current_app.scheduler.get_job(job_id).pause()
    return jsonify(str(response))

@api_blueprint.route("/<job_id>/resume")
def job_resume(job_id):
    response = current_app.scheduler.get_job(job_id).resume()
    return jsonify(str(response))

@api_blueprint.route("/<job_id>/remove")
def job_remove(job_id):
    current_app.scheduler.get_job(job_id).remove()
    return jsonify("Job #{} Removed".format(job_id))
