"""Error Handlers"""
from flask import Blueprint, redirect, render_template, session, url_for
from . import login_manager
handler = Blueprint("handler", __name__)

@login_manager.unauthorized_handler
def not_logined():
    # session["login_message_body"] = "You Must Login First"
    # session["login_message_type"] = "warning"
    return redirect(url_for("user.login"))

@handler.errorhandler(401)
def page_unauthorized(error):
    """A Page Not Found Handler"""
    return render_template("error.html", error=error), 401

@handler.errorhandler(404)
def page_not_found(error):
    """A Page Not Found Handler"""
    return render_template("error.html", error=error), 404
