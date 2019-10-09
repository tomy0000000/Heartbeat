"""Forms"""
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

class CronForm(FlaskForm):
    year = wtforms.IntegerField("Year")
    month = wtforms.IntegerField("Month")
    day = wtforms.IntegerField("Day")
    week = wtforms.IntegerField("Week")
    day_of_week = wtforms.RadioField("Day of Week", choices=[
        ("mon", "Monday"),
        ("tue", "Tuesday"),
        ("wed", "Wednesday"),
        ("thu", "Thursday"),
        ("fri", "Friday"),
        ("sat", "Saturday"),
        ("sun", "Sunday")
    ])
    hour = wtforms.IntegerField("Hour")
    minute = wtforms.IntegerField("Minute")
    second = wtforms.IntegerField("Second")
    start_date = wtforms.DateTimeField("Start Date")
    end_date = wtforms.DateTimeField("End Date")
    # timezone = wtforms.DateTimeField("Timezone")
    jitter = wtforms.IntegerField("Jitter")

class DateForm(FlaskForm):
    run_date = wtforms.DateTimeField("Run Date")
    # timezone = wtforms.DateTimeField("Timezone")

class IntervalForm(FlaskForm):
    weeks = wtforms.DateField("Weeks")
    days = wtforms.DateField("Days")
    hours = wtforms.DateField("Hours")
    minutes = wtforms.DateField("Minutes")
    seconds = wtforms.DateField("Seconds")
    start_date = wtforms.DateTimeField("Start Date")
    end_date = wtforms.DateTimeField("End Date")
    # timezone = wtforms.DateTimeField("Timezone")
    jitter = wtforms.IntegerField("Jitter")

class JobForm(FlaskForm):
    id = wtforms.StringField("Job ID", validators=[
        wtforms.validators.InputRequired(),
        wtforms.validators.Length(min=3, max=10)
    ])
    name = wtforms.StringField("Job Name", validators=[
        wtforms.validators.InputRequired(),
        wtforms.validators.Length(min=3, max=10)
    ])
    func = wtforms.SelectField("Function")
    args = wtforms.StringField("Arguments")
    kwargs = wtforms.StringField("Keyword Arguments")
    coalesce = wtforms.BooleanField("Coalesce")
    trigger = wtforms.SelectField("Trigger", choices=[
        ("cron", "Cron"),
        ("date", "Date"),
        ("interval", "Interval")
    ])
    # Implement Dynamic Trigger Args Fields
    cron_trigger_args = wtforms.FormField(CronForm)
    date_trigger_args = wtforms.FormField(DateForm)
    interval_trigger_args = wtforms.FormField(IntervalForm)
    executor = wtforms.StringField("Executor")
    misfire_grace_time = wtforms.IntegerField("Misfire Grace Time")
    max_instances = wtforms.IntegerField("Max Instances")
    next_run_time = wtforms.DateTimeField("Next Run Time")
    replace_existing = wtforms.BooleanField("Replace Existing")
    type = wtforms.HiddenField("Type")
    submit = wtforms.SubmitField("Apply")
