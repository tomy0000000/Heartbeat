# TSkr

This is a legacy version of TSkr, which build on top of [APScheduler](https://github.com/agronholm/apscheduler) with the assist of [Flask-APScheduler](https://github.com/viniciuschiele/flask-apscheduler).

As this setup doesn't compatible with my current deployment stack (nginx+uwsgi+flask).

The app has been rebuilt from ground up with a new backend system, if you're interested, please headover to [TSkr](https://github.com/tomy0000000/TSkr)

## Installation

* Clone repository

```bash
git clone https://github.com/tomy0000000/TSkr-legacy.git
cd TSkr-legacy
```

* Install Packages (pipenv is suggested)

```bash
pipenv install
```

## Run

* Patch your configuration in `deploy/uwsgi.ini`

* Run

```
uwsgi deploy/uwsgi.ini
```

