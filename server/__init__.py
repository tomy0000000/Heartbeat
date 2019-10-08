"""Core Service of Hearbeat"""
import inspect
import logging
import rpyc
from rpyc.utils.server import ThreadedServer
from apscheduler.schedulers.background import BackgroundScheduler
from .task.example import date_func, interval_func, cron_func

class SchedulerService(rpyc.Service):
    def __init__(self, **config):
        self._scheduler = BackgroundScheduler()
        self._scheduler.configure(**config)
        self._scheduler.start()
        self.logger = logging.getLogger("Heartbeat.core")
        self.logger.info("Heartbeat Core Initalized")
    def on_connect(self, conn):
        self.logger.info("----------Begin New Client----------")
        self.logger.info(conn)
        self.logger.info("----------End New Client----------")
        # code that runs when a connection is created
        # (to init the service, if needed)
        pass
    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        pass
    def exposed_add_job(self, func, *args, **kwargs):
        self.logger.info("----------Begin New Job----------")
        # self.logger.info("ID: #{}".format(id))
        self.logger.info("Function: %s", str(func))
        self.logger.info("*args: %s", str(args))
        self.logger.info("**kwargs: %s", str(dict(kwargs)))
        self.logger.info("----------Eng New Job----------")
        return self._scheduler.add_job(func, *args, **kwargs)
    def exposed_modify_job(self, job_id, jobstore=None, **changes):
        return self._scheduler.modify_job(job_id, jobstore, **changes)
    def exposed_reschedule_job(self, job_id, jobstore=None, trigger=None, **trigger_args):
        return self._scheduler.reschedule_job(job_id, jobstore, trigger, **trigger_args)
    def exposed_pause_job(self, job_id, jobstore=None):
        return self._scheduler.pause_job(job_id, jobstore)
    def exposed_resume_job(self, job_id, jobstore=None):
        return self._scheduler.resume_job(job_id, jobstore)
    def exposed_remove_job(self, job_id, jobstore=None):
        self._scheduler.remove_job(job_id, jobstore)
    def exposed_get_job(self, job_id, jobstore=None):
        return self._scheduler.get_job(job_id, jobstore=jobstore)
    def exposed_get_jobs(self, jobstore=None):
        results = self._scheduler.get_jobs(jobstore)
        return results
    def exposed_configure(self, gconfig={}, prefix="apscheduler.", **options):
        """A Shallow Function Kept to compatible with flask-apscheduler"""
        # self._scheduler.configure(gconfig, prefix, **options)
        pass
    def exposed_start(self, paused=False):
        """A Shallow Function Kept to compatible with flask-apscheduler"""
        # self._scheduler.start(paused)
    def exposed_get_tasks(self):
        """Return a list of schedule-able function"""
        tasks = []
        cloned_globals = globals()
        for name, ref in cloned_globals.items():
            namespace = inspect.getmodule(ref).__name__
            if callable(ref) and namespace.startswith("server.task"):
                tasks.append("{}:{}".format(namespace, name))
        return tasks
