"""Login Blueprint"""
from datetime import datetime
from flask import Blueprint, current_app, redirect, session, url_for, render_template
from flask_login import current_user, login_required, login_user, logout_user
from .. import login_manager
from ..forms import LoginForm
from ..helper import send_notification
from ..models import Users
user_blueprint = Blueprint("user", __name__)

login_manager.login_view = "user.login"
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        session["alert"] = "You've already logined!"
        session["alert_type"] = "success"
        return redirect(url_for("main.dashboard"))
    form = LoginForm()
    alert = session.pop("login_message_body", None)
    alert_type = session.pop("login_message_type", None)
    if form.validate_on_submit():
        query_user = Users.query.filter_by(username=form.username.data).first()
        if query_user and query_user.check_password(form.password.data):
            login_user(query_user)
            return redirect(url_for("main.dashboard"))
        alert = "Invalid username or password."
        alert_type = "warning"
    return render_template("login.html",
                           form=form,
                           alert=alert,
                           alert_type=alert_type)

@user_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    session["login_message_body"] = "You've Logged Out"
    session["login_message_type"] = "success"
    return redirect(url_for("user.login"))
