# TSkr

TSkr is a web-based scheduler executer, features simple user interface for task managing.

The core is build on top of [APScheduler](https://github.com/agronholm/apscheduler) with the assist of [Flask-APScheduler](https://github.com/viniciuschiele/flask-apscheduler).

## Installation

* Clone repository

```bash
git clone https://github.com/tomy0000000/TSkr.git
cd TSkr
```

* Install Packages (pipenv is suggested)

```bash
pipenv install
```

## Configure

* Copy Deployment Script

````bash
mkdir instance
cd deploy
cp uwsgi.ini ../instance/uwsgi.ini
# Following Path fits for Ubuntu
(sudo) cp TSkr-client.service /etc/systemd/system
(sudo) cp TSkr-core.service /etc/systemd/system
(sudo) cp TSkr-main.target /etc/systemd/system
````

* Edit `TSkr-client.service `, `TSkr-core.service`

* Add Environmental Variables

```python
# /var/www/TSkr/.env
SERVER_NAME=
SECRET_KEY=
DATABASE_URL=
```

## Run

* Activate Service

```bash
(sudo) systemctl daemon-reload
(sudo) systemctl enable TSkr-client.service
(sudo) systemctl enable TSkr-core.service
(sudo) systemctl enable TSkr-main.target
(sudo) systemctl start TSkr-main.target
```



