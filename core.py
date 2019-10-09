"""Bootscript for Heartbeat Core Server"""
import os
import logging.config
from rpyc.utils.server import ThreadedServer
from rpyc.utils.authenticators import SSLAuthenticator
from server import SchedulerService
from config_server import (
    SERVER_PORT,
    PROTOCOL_CONFIG,
    SERVER_SSL_KEYFILE,
    SERVER_SSL_CERTFILE,
    SCHEDULER_CONFIG,
    LOGGING_CONFIG
)
logging.config.dictConfig(LOGGING_CONFIG)

if __name__ == "__main__":
    if SERVER_SSL_KEYFILE and SERVER_SSL_CERTFILE:
        key_path = os.path.join(os.path.dirname(__file__), "instance", SERVER_SSL_KEYFILE)
        cert_path = os.path.join(os.path.dirname(__file__), "instance", SERVER_SSL_CERTFILE)
        if os.path.exists(key_path) and os.path.exists(cert_path):
            authenticator = SSLAuthenticator(key_path, cert_path)
            logging.info("SSL Activated")
    else:
        authenticator = None
    server = ThreadedServer(
        SchedulerService(**SCHEDULER_CONFIG),
        port=SERVER_PORT,
        protocol_config=PROTOCOL_CONFIG,
        authenticator=authenticator
    )
    server.start()
