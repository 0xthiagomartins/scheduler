# scheduler_service.py

from schedule import Scheduler
import threading
import time


class SchedulerService:
    name = "scheduler_service"

    def __init__(self):
        self.scheduler = Scheduler()
        self.jobs = {}
        self._start_scheduler()

    def _start_scheduler(self):
        def run_continuously():
            while True:
                self.scheduler.run_pending()
                time.sleep(1)

        t = threading.Thread(target=run_continuously)
        t.daemon = True
        t.start()

    def add_job(self, job_name, interval, unit, action):
        if unit == "seconds":
            self.jobs[job_name] = self.scheduler.every(interval).seconds.do(action)
        elif unit == "minutes":
            self.jobs[job_name] = self.scheduler.every(interval).minutes.do(action)
        elif unit == "hours":
            self.jobs[job_name] = self.scheduler.every(interval).hours.do(action)
        else:
            return "Invalid time unit. Use 'seconds', 'minutes', or 'hours'."
        return f"Job {job_name} added."

    def remove_job(self, job_name):
        if job_name in self.jobs:
            self.scheduler.cancel_job(self.jobs[job_name])
            del self.jobs[job_name]
            return f"Job {job_name} removed."
        return f"Job {job_name} not found."

    def list_jobs(self):
        job_list = {job_name: str(job) for job_name, job in self.jobs.items()}
        return job_list
