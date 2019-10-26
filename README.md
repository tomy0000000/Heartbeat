# Heartbeat💓

![Python Version](https://img.shields.io/badge/python-3.4+-blue.svg)
[![Build Status](https://travis-ci.com/tomy0000000/Heartbeat.svg?branch=master)](https://travis-ci.com/tomy0000000/Heartbeat)
[![liscense](https://img.shields.io/github/license/tomy0000000/Heartbeat.svg)](https://github.com/tomy0000000/Heartbeat/blob/master/LICENSE)

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
SERVER_SSL_KEYFILE= # Optional, "server.key" if you followed the script
SERVER_SSL_CERTFILE= # Optional, "server-cert.pem" if you followed the script
CLIENT_SSL_KEYFILE= # Optional, "client.key" if you followed the script
CLIENT_SSL_CERTFILE= # Optional, "client-cert.pem" if you followed the script
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

## Create Client & Server Certificate

* Create CA Certificate

```bash
openssl genrsa 2048 > ca-key.pem
openssl req -new -sha256 -x509 -nodes -days 3600 -key ca-key.pem -out ca-cert.pem
# Fill the Form, or just leave everything empty
```

* Create Client Certificate

```bash
openssl req -sha256 -newkey rsa:2048 -days 3600 -nodes -keyout client.key -out client-req.csr
openssl rsa -in client.key -out client.key
openssl x509 -sha256 -req -in client-req.csr -days 3600 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out client-cert.pem
rm client-req.csr
```

* Create Server Certificate

```bash
openssl req -sha256 -newkey rsa:2048 -days 3600 -nodes -keyout server.key -out server-req.csr
openssl rsa -in server.key -out server.key
openssl x509 -sha256 -req -in server-req.csr -days 3600 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out server-cert.pem
rm server-req.csr
```