"""Forms"""
from wtforms.fields import (
    BooleanField,
    # DateTimeLocalField,
    FormField,
    HiddenField,
    # IntegerField,
    PasswordField,
    RadioField,
    SelectField,
    StringField,
    SubmitField
)
from wtforms.fields.html5 import (
    DateTimeLocalField,
    IntegerField
)
from wtforms.validators import (
    DataRequired,
    InputRequired,
    Length,
    NumberRange,
    Optional
)
from flask import current_app
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[
        InputRequired(), Length(min=3, max=20)
    ])
    password = PasswordField("Password", validators=[
        InputRequired(), Length(min=3, max=20)
    ])
    submit = SubmitField("Sign In")

class JobBaseForm(FlaskForm):
    job_id = StringField("Job ID", validators=[
        InputRequired(), Length(min=3, max=10)
    ], render_kw={
        "class": "form-control"
    })
    job_name = StringField("Job Name", validators=[
        InputRequired(), Length(min=3, max=10)
    ], render_kw={
        "class": "form-control"
    })
    func = SelectField("Function", validators=[
        DataRequired()
    ], render_kw={
        "class": "form-control"
    })
    args = StringField("Arguments", render_kw={
        "class": "form-control",
        "readonly": ""
    })
    kwargs = StringField("Keyword Arguments", render_kw={
        "class": "form-control",
        "readonly": ""
    })
    coalesce = BooleanField("Coalesce", render_kw={
        "class": "custom-control-input",
        "disabled": ""
    })
    trigger = RadioField("Trigger", validators=[
        DataRequired()
    ], choices=[
        ("cron", "Cron"),
        ("date", "Date"),
        ("interval", "Interval")
    ])
    executor = StringField("Executor", validators=[
        Optional()
    ], render_kw={
        "class": "form-control",
        "readonly": ""
    })
    misfire_grace_time = IntegerField("Misfire Grace Time", validators=[
        Optional()
    ], render_kw={
        "class": "form-control",
        "readonly": ""
    })
    max_instances = IntegerField("Max Instances", validators=[
        Optional()
    ], render_kw={
        "class": "form-control",
        "readonly": ""
    })
    next_run_time = DateTimeLocalField("Next Run Time", validators=[
        Optional()
    ], render_kw={
        "class": "form-control",
        "readonly": ""
    }, format="%Y-%m-%dT%H:%M:%S")
    replace_existing = BooleanField("Replace Existing", render_kw={
        "class": "custom-control-input",
        "disabled": ""
    })

class CronForm(FlaskForm):
    year = StringField("Year", render_kw={
        "class": "form-control"
    })
    month = StringField("Month", render_kw={
        "class": "form-control"
    })
    day = StringField("Day", render_kw={
        "class": "form-control"
    })
    week = StringField("Week", render_kw={
        "class": "form-control"
    })
    day_of_week = StringField("Day of Week", render_kw={
        "class": "form-control"
    })
    hour = StringField("Hour", render_kw={
        "class": "form-control"
    })
    minute = StringField("Minute", render_kw={
        "class": "form-control"
    })
    second = StringField("Second", render_kw={
        "class": "form-control"
    })
    start_date = DateTimeLocalField("Start Date", validators=[
        Optional()
    ], render_kw={
        "class": "form-control",
        "step": "1"
    }, format="%Y-%m-%dT%H:%M:%S")
    end_date = DateTimeLocalField("End Date", validators=[
        Optional()
    ], render_kw={
        "class": "form-control",
        "step": "1"
    }, format="%Y-%m-%dT%H:%M:%S")
    timezone = DateTimeLocalField("Timezone", validators=[
        Optional()
    ], render_kw={
        "class": "form-control",
        "readonly": ""
    })
    jitter = IntegerField("Jitter", validators=[
        Optional()
    ], render_kw={
        "class": "form-control",
        "readonly": ""
    })
    def validate(self):
        param = [
            self.year,
            self.month,
            self.day,
            self.week,
            self.day_of_week,
            self.hour,
            self.minute,
            self.second
        ]
        for field in param:
            if field.data:
                return True
        # Fallback to here means none of the fields is filled
        self.day_of_week.errors = ["Fill at least one of them."]
        for field in param:
            field.errors = ["Fill at least one of them."]
        return False

class DateForm(FlaskForm):
    run_date = DateTimeLocalField("Run Date", validators=[
        InputRequired()
    ], render_kw={
        "class": "form-control",
        "step": "1"
    }, format="%Y-%m-%dT%H:%M:%S")
    timezone = DateTimeLocalField("Timezone", validators=[
        Optional()
    ], render_kw={
        "class": "form-control",
        "readonly": ""
    })

class IntervalForm(FlaskForm):
    weeks = IntegerField("Weeks", validators=[
        Optional(),
        NumberRange(min=1)
    ], render_kw={
        "class": "form-control",
        "min": "1"
    })
    days = IntegerField("Days", validators=[
        Optional(),
        NumberRange(min=1)
    ], render_kw={
        "class": "form-control",
        "min": "1"
    })
    hours = IntegerField("Hours", validators=[
        Optional(),
        NumberRange(min=1)
    ], render_kw={
        "class": "form-control",
        "min": "1"
    })
    minutes = IntegerField("Minutes", validators=[
        Optional(),
        NumberRange(min=1)
    ], render_kw={
        "class": "form-control",
        "min": "1"
    })
    seconds = IntegerField("Seconds", validators=[
        Optional(),
        NumberRange(min=1)
    ], render_kw={
        "class": "form-control",
        "min": "1"
    })
    start_date = DateTimeLocalField("Start Date", validators=[
        Optional()
    ], render_kw={
        "class": "form-control",
        "step": "1"
    }, format="%Y-%m-%dT%H:%M:%S")
    end_date = DateTimeLocalField("End Date", validators=[
        Optional()
    ], render_kw={
        "class": "form-control",
        "step": "1"
    }, format="%Y-%m-%dT%H:%M:%S")
    timezone = DateTimeLocalField("Timezone", validators=[
        Optional()
    ], render_kw={
        "class": "form-control",
        "readonly": ""
    })
    jitter = IntegerField("Jitter", validators=[
        Optional()
    ], render_kw={
        "class": "form-control",
        "readonly": ""
    })
    def validate(self):
        param = [
            self.weeks,
            self.days,
            self.hours,
            self.minutes,
            self.seconds
        ]
        for field in param:
            if field.data:
                return True
        # Fallback to here means none of the fields is filled
        for field in param:
            field.errors = ["Fill at least one of them."]
        return False

class JobForm(FlaskForm):
    base_args = FormField(JobBaseForm)
    cron_trigger_args = FormField(CronForm)
    date_trigger_args = FormField(DateForm)
    interval_trigger_args = FormField(IntervalForm)
    type = HiddenField("Type")
    submit = SubmitField("Apply")
    def validate(self):
        current_app.logger.info("----------BEGIN FORM VALIDATE----------")
        results = True
        if not FlaskForm.validate(self.base_args.form):
            current_app.logger.info("Base Form Not Validate")
            results = False
        if self.base_args.trigger.data == "cron" and not self.cron_trigger_args.validate(self):
            current_app.logger.info("Cron Form Not Validate")
            results = False
        if self.base_args.trigger.data == "date" and not self.date_trigger_args.validate(self):
            current_app.logger.info("Date Form Not Validate")
            results = False
        if self.base_args.trigger.data == "interval" and not self.interval_trigger_args.validate(self):
            current_app.logger.info("Interval Form Not Validate")
            results = False
        current_app.logger.info("Final Results: {}".format(results))
        current_app.logger.info("----------END FORM VALIDATE----------")
        return results
