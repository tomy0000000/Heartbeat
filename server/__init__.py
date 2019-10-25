"""Core Service of Hearbeat"""
import os
import importlib
import inspect
import logging
from datetime import datetime
import rpyc
from rpyc.utils.server import ThreadedServer
from apscheduler.schedulers.background import BackgroundScheduler

class SchedulerService(rpyc.Service):
    def __init__(self, **config):
        self._scheduler = BackgroundScheduler()
        self._scheduler.configure(**config)
        self._scheduler.start()
        self.logger = logging.getLogger("Heartbeat.core")
        self.logger.info("Heartbeat Core Initalized")
    def on_connect(self, conn):
        # code that runs when a connection is created
        # (to init the service, if needed)
        self.logger.info("----------Begin New Client----------")
        self.logger.info(conn)
        self.logger.info("----------End New Client----------")
    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        self.logger.info("----------Begin Goodbye Client----------")
        self.logger.info(conn)
        self.logger.info("----------End Goodbye Client----------")
    def exposed_add_job(self, func, *args, **kwargs):
        self.logger.info("----------Begin New Job----------")
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
    def exposed_get_tasks(self):
        """Return a list of schedule-able function"""
        tasks = []
        for module_file in os.listdir(os.path.join(os.path.dirname(__file__), "task")):
            if module_file == "__init__.py" or module_file[-3:] != ".py":
                continue
            module_name = "server.task.{}".format(module_file[:-3])
            module = importlib.import_module(module_name)
            if not hasattr(module, "__all__"):
                continue
            for function_name in module.__all__:
                function = getattr(module, function_name)
                if not callable(function):
                    continue
                parameters = inspect.signature(function).parameters
                parameters_str = ", ".join([str(val) for key, val in parameters.items()])
                tasks.append("{}:{}({})".format(module_name, function_name, parameters_str))
        return tasks
