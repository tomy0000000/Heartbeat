"""Login Blueprint"""
from datetime import datetime
from flask import Blueprint, redirect, session, url_for, render_template
from flask_login import current_user, login_required, login_user, logout_user
from .. import login_manager
from ..forms import LoginForm
from ..helper import send_notification
from ..models import Users
login_blueprint = Blueprint("login", __name__)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

@login_manager.unauthorized_handler
def not_logined():
    session["login_message_body"] = "You Must Login First"
    session["login_message_type"] = "warning"
    return redirect(url_for("login.login"))

@login_blueprint.errorhandler(401)
def page_unauthorized(error):
    """A Page Not Found Handler"""
    send_notification("401 Alert", str(datetime.now()),
                      title="TSkr received an 401 Error!!")
    return render_template("error.html", error=error), 401

@login_blueprint.errorhandler(404)
def page_not_found(error):
    """A Page Not Found Handler"""
    send_notification("404 Alert", str(datetime.now()),
                      title="TSkr received an 404 Error!!")
    return render_template("error.html", error=error), 404

@login_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        session["alert"] = "You've already logined!"
        session["alert_type"] = "success"
        return redirect(url_for("main.dashboard"))
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        query_user = Users.query.filter_by(username=form.username.data).first()
        if query_user and query_user.valid_password(form.password.data):
            login_user(query_user)
            return redirect(url_for("secret"))
        error = "Invalid username or password."
    return render_template("login.html", form=form, error=error)

@login_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@login_blueprint.route("/secret")
@login_required
def secret():
    return render_template("empty.html",
                           content="Welcome, {}".format(current_user.username))
