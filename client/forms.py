"""Forms of TSkr"""
import wtforms
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    username = wtforms.StringField("Username", validators=[
        wtforms.validators.InputRequired(),
        wtforms.validators.Length(min=3, max=20)
    ])
    password = wtforms.PasswordField("Password", validators=[
        wtforms.validators.InputRequired(),
        wtforms.validators.Length(min=3, max=20)
    ])
    submit = wtforms.SubmitField("Sign In")

class JobForm(FlaskForm):
    id = wtforms.StringField("Job ID", validators=[
        wtforms.validators.InputRequired(),
        wtforms.validators.Length(min=3, max=10)
    ])
    name = wtforms.StringField("Job Name", validators=[
        wtforms.validators.InputRequired(),
        wtforms.validators.Length(min=3, max=10)
    ])
    func = wtforms.StringField("Function")
    args = wtforms.StringField("Arguments")
    kwargs = wtforms.StringField("Keyword Arguments")
    coalesce = wtforms.BooleanField("Coalesce")
    trigger = wtforms.SelectField("Trigger", choices=[
        ("cron", "Cron"),
        ("date", "Date"),
        ("interval", "Interval")
    ])
    executor = wtforms.StringField("Executor")
    misfire_grace_time = wtforms.IntegerField("Misfire Grace Time")
    max_instances = wtforms.IntegerField("Max Instances")
    next_run_time = wtforms.DateTimeField("Next Run Time")
    type = wtforms.HiddenField("Type")
    submit = wtforms.SubmitField("Apply")
