from nameko.rpc import rpc
from apscheduler.schedulers.background import BackgroundScheduler
from sqlmodel import create_engine
from .business.executor import TaskExecutor
from .business.manager import TaskManager
from .business.in_memory import redis_client
from .business.models import SQLModel
import pika, os, json


class SchedulerService:
    name = "scheduler"

    def __init__(self):
        rabbitmq_host = os.getenv("RABBITMQ_HOST", "localhost")
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbitmq_host)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="task_queue", durable=True)

        db_url = os.getenv("DATABASE_URL")
        self.engine = create_engine(db_url)
        SQLModel.metadata.create_all(self.engine)

        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

        self.executor = TaskExecutor(self.engine)
        self.manager = TaskManager(self.engine)

    def send_task(
        self,
        service_name: str,
        service_method: str,
        args: list,
        kwargs: dict,
        attempts: int,
        max_attempts: int,
    ):
        if attempts > max_attempts:
            return

        self.channel.basic_publish(
            exchange="",
            routing_key="task_queue",
            body=json.dumps(
                {
                    "service_name": service_name,
                    "service_method": service_method,
                    "args": args,
                    "kwargs": kwargs,
                    "attempts": attempts,
                    "max_attempts": max_attempts,
                }
            ),
            properties=pika.BasicProperties(
                delivery_mode=2,
            ),
        )

    def parse_cron(self, cron: str):
        cron_parts = cron.split()
        return {
            "second": cron_parts[0],
            "minute": cron_parts[1],
            "hour": cron_parts[2],
            "day": cron_parts[3],
            "month": cron_parts[4],
            "day_of_week": cron_parts[5],
        }

    @rpc
    def schedule_task(
        self,
        cron: str,
        service_name: str,
        service_method: str,
        args: list,
        kwargs: dict,
        max_attempts: int = 3,
    ):
        cron_params = self.parse_cron(cron)
        self.scheduler.add_job(
            self.send_task,
            "cron",
            args=[service_name, service_method, args, kwargs, 0, max_attempts],
            **cron_params,
        )
        return {
            "message": f"Scheduled {service_name}.{service_method} with cron {cron}"
        }

    @rpc
    def execute_task(
        self,
        service_name: str,
        service_method: str,
        args: list,
        kwargs: dict,
        attempts: int,
        max_attempts: int,
    ):
        self.executor.execute_task(
            service_name, service_method, args, kwargs, attempts, max_attempts
        )

    @rpc
    def get_task_logs(self):
        return self.manager.get_task_logs()

    @rpc
    def get_task_metrics(self):
        return self.manager.get_task_metrics()

    @rpc
    def shutdown(self):
        self.scheduler.shutdown()
        self.connection.close()
