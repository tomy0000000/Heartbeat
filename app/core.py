#! /home/tomy0000000/.local/share/virtualenvs/TSkr-laitjqxb/bin/python
"""
This is an example showing how to make the scheduler into a remotely accessible service.
It uses RPyC to set up a service through which the scheduler can be made to add, modify and remove
jobs.

To run, first install RPyC using pip. Then change the working directory to the ``rpc`` directory
and run it with ``python -m server``.
"""
import rpyc
import time
from rpyc.utils.server import ThreadedServer
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

def print_text(text):
    logging.info(text)

class SchedulerService(rpyc.Service):
    def exposed_add_job(self, func, *args, **kwargs):
        return scheduler.add_job(func, *args, **kwargs)
    def exposed_modify_job(self, job_id, jobstore=None, **changes):
        return scheduler.modify_job(job_id, jobstore, **changes)
    def exposed_reschedule_job(self, job_id, jobstore=None, trigger=None, **trigger_args):
        return scheduler.reschedule_job(job_id, jobstore, trigger, **trigger_args)
    def exposed_pause_job(self, job_id, jobstore=None):
        return scheduler.pause_job(job_id, jobstore)
    def exposed_resume_job(self, job_id, jobstore=None):
        return scheduler.resume_job(job_id, jobstore)
    def exposed_remove_job(self, job_id, jobstore=None):
        scheduler.remove_job(job_id, jobstore)
    def exposed_get_job(self, job_id):
        return scheduler.get_job(job_id)
    def exposed_get_jobs(self, jobstore=None):
        results = scheduler.get_jobs(jobstore)
        logging.info(results)
        return results
    def exposed_configure(self, gconfig={}, prefix="apscheduler.", **options):
        logging.info("-------------------")
        logging.info(gconfig)
        logging.info("-------------------")
        logging.info(prefix)
        logging.info("-------------------")
        logging.info(options)
        scheduler.configure(gconfig, prefix, **options)
    def exposed_start(self, paused=False):
        logging.info("TSkr Core Started!!!")
        scheduler.start(paused)

import logging
logging.basicConfig(filename="/var/www/TSkr/log/core.log", level=logging.DEBUG)

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    # scheduler.start()
    protocol_config = {"allow_public_attrs": True}
    server = ThreadedServer(SchedulerService, port=4792, protocol_config=protocol_config)
    logging.info("TSkr Core Launched!!!")
    server.start()
