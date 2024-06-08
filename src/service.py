from .business import SchedulerService
from nameko.rpc import rpc


class SchedulerRPC:
    name = "scheduler"

    def __init__(self):
        self.scheduler = SchedulerService()

    @rpc
    def add_job(self, name, interval, unit, action):
        return self.scheduler.add_job(name, interval, unit, action)

    @rpc
    def remove_job(self, name):
        return self.scheduler.remove_job(name)

    @rpc
    def list_jobs(self):
        return self.scheduler.list_jobs()
