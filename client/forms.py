"""Forms"""
import wtforms
from wtforms.fields import (
    BooleanField,
    # DateTimeLocalField,
    FormField,
    HiddenField,
    # IntegerField,
    PasswordField,
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
        "id": "job_id",
        "class": "form-control"
    })
    job_name = StringField("Job Name", validators=[
        InputRequired(), Length(min=3, max=10)
    ], render_kw={
        "id": "job_name",
        "class": "form-control"
    })
    func = SelectField("Function", validators=[
        DataRequired()
    ], render_kw={
        "id": "func",
        "class": "form-control"
    })
    args = StringField("Arguments", render_kw={
        "id": "args",
        "class": "form-control",
        "readonly": ""
    })
    kwargs = StringField("Keyword Arguments", render_kw={
        "id": "kwargs",
        "class": "form-control",
        "readonly": ""
    })
    coalesce = BooleanField("Coalesce", render_kw={
        "class": "custom-control-input",
        "disabled": ""
    })
    trigger = SelectField(
        "Trigger",
        render_kw={
            "id": "trigger",
            "class": "form-control",
        },
        choices=[
            ("", ""),
            ("cron", "Cron"),
            ("date", "Date"),
            ("interval", "Interval")
        ], validators=[
            DataRequired()
        ])
    executor = StringField("Executor")
    misfire_grace_time = IntegerField("Misfire Grace Time", validators=[
        Optional()
    ])
    max_instances = IntegerField("Max Instances", validators=[
        Optional()
    ])
    next_run_time = DateTimeLocalField("Next Run Time", validators=[
        Optional()
    ])
    replace_existing = BooleanField("Replace Existing")

class CronForm(FlaskForm):
    year = IntegerField("Year"
    #     , validators=[
    #     wtforms.validators.NumberRange(min=None, max=9999)
    # ]
    )
    month = IntegerField("Month")
    day = IntegerField("Day")
    week = IntegerField("Week")
    day_of_week = wtforms.RadioField("Day of Week", choices=[
        ("mon", "Monday"),
        ("tue", "Tuesday"),
        ("wed", "Wednesday"),
        ("thu", "Thursday"),
        ("fri", "Friday"),
        ("sat", "Saturday"),
        ("sun", "Sunday")
    ])
    hour = IntegerField("Hour")
    minute = IntegerField("Minute")
    second = IntegerField("Second")
    start_date = DateTimeLocalField("Start Date")
    end_date = DateTimeLocalField("End Date")
    timezone = DateTimeLocalField("Timezone")
    jitter = IntegerField("Jitter")

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
        # results = False
        results = True
        current_app.logger.info("Interval Form Start Validating")
        if not self.weeks.data \
        and not self.days.data \
        and not self.hours.data \
        and not self.minutes.data \
        and not self.seconds.data:
            current_app.logger.info("Validate Failed")
            results = False
            for field in [self.weeks, self.days, self.hours, self.minutes, self.seconds]:
                field.errors = "Fill at least one of them."
                current_app.logger.info("{} errors set".format(field.name))
                # current_app.logger.info("{}: {}".format(field.name, field.errors))
                # field.errors.append("Fill at least one of them.")
        return results

class JobForm(FlaskForm):
    base_args = FormField(JobBaseForm)
    cron_trigger_args = FormField(CronForm)
    date_trigger_args = FormField(DateForm)
    interval_trigger_args = FormField(IntervalForm)
    type = HiddenField("Type")
    submit = SubmitField("Apply")
    def validate(self):
        results = True
        if not FlaskForm.validate(self.base_args.form):
            current_app.logger.info("Base Form Not Validate")
            results = False
        # current_app.logger.info("Cron: {}".format(FlaskForm.validate(self.cron_trigger_args.form)))
        if self.base_args.trigger.data == "cron" and not FlaskForm.validate(self.cron_trigger_args.form):
            results = False
        # current_app.logger.info("Date: {}".format(FlaskForm.validate(self.date_trigger_args.form)))
        if self.base_args.trigger.data == "date" and not FlaskForm.validate(self.date_trigger_args.form):
            results = False
        current_app.logger.info(
            "Interval FormField: {}".format(
                # FlaskForm.validate(self.interval_trigger_args.form)
                self.interval_trigger_args.validate(self)
            )
        )
        current_app.logger.info(
            "Interval Form: {}".format(
                # FlaskForm.validate(self.interval_trigger_args.form)
                self.interval_trigger_args.form.validate()
            )
        )
        current_app.logger.info(
            "Interval Form Flask: {}".format(
                FlaskForm.validate(self.interval_trigger_args.form)
                # self.interval_trigger_args.validate(self)
            )
        )
        if self.base_args.trigger.data == "interval" and not FlaskForm.validate(self.interval_trigger_args.form):
            results = False
        return results
