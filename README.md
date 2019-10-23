# Heartbeat💓

Heartbeat is a task manager/scheduler/executer, features multiple interfaces for managing.

The core is build on top of [APScheduler](https://github.com/agronholm/apscheduler) & [RPyC](https://github.com/tomerfiliba/rpyc).

## Installation

* Clone repository

```bash
git clone https://github.com/tomy0000000/Heartbeat.git
cd Heartbeat
```

* Install Packages (pipenv is suggested)

```bash
pipenv install
```

## Configure

* Copy Deployment Script

````bash
mkdir instance
cd instance && cp ../deploy/uwsgi.ini .
# Following Path fits for Ubuntu
(sudo) cp Heartbeat-client.service /etc/systemd/system
(sudo) cp Heartbeat-core.service /etc/systemd/system
(sudo) cp Heartbeat-main.target /etc/systemd/system
````

* Edit `Heartbeat-client.service`, `Heartbeat-core.service`

* Add Environmental Variables

```python
# /var/www/Heartbeat/.env
CLIENT_SERVER_NAME= # Optional
CLIENT_APPLICATION_ROOT= # Optional
SECRET_KEY=
DATABASE_URL=
SERVER_SSL_KEYFILE= # Optional
SERVER_SSL_CERTFILE= # Optional
CLIENT_SSL_KEYFILE= # Optional
CLIENT_SSL_CERTFILE= # Optional
```

## Run

* Activate Service

```bash
(sudo) systemctl daemon-reload
(sudo) systemctl enable Heartbeat-client.service
(sudo) systemctl enable Heartbeat-core.service
(sudo) systemctl enable Heartbeat-main.target
(sudo) systemctl start Heartbeat-main.target
```

## Local Development

* Run Core Server

```bash
python core.py
```

* Run Client App (Execute in a different shell)

```bash
export FLASK_ENV=development
flask run
```

