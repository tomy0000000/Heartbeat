"""Bootscript for Heartbeat Core Server"""
import logging
from rpyc.utils.server import ThreadedServer
from server import SchedulerService
from config_server import config
logging.basicConfig(filename="log/core.log", level=logging.INFO)

if __name__ == "__main__":
    protocol_config = {"allow_public_attrs": True}
    server = ThreadedServer(SchedulerService(**config), port=4792, protocol_config=protocol_config)
    logging.info("Heartbeat Core Launched")
    server.start()
