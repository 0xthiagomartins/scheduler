from nameko.rpc import RpcProxy
from sqlmodel import Session
from .models import TaskLog
from .in_memory import redis_client
import json


class TaskExecutor:
    def __init__(self, engine):
        self.engine = engine
        self.rpc_proxy = RpcProxy()

    def execute_task(
        self,
        service_name: str,
        service_method: str,
        args: list,
        kwargs: dict,
        attempts: int,
        max_attempts: int,
    ):
        try:
            service = getattr(self.rpc_proxy, service_name)
            method = getattr(service, service_method)
            result = method(*args, **kwargs)
            status = "success"
        except Exception as e:
            status = "failed"
            if attempts < max_attempts:
                self.schedule_retry(
                    service_name,
                    service_method,
                    args,
                    kwargs,
                    attempts + 1,
                    max_attempts,
                )

        with Session(self.engine) as session:
            task_log = TaskLog(
                task_name=f"{service_name}.{service_method}",
                args=json.dumps(args),
                kwargs=json.dumps(kwargs),
                status=status,
                attempts=attempts,
                max_attempts=max_attempts,
            )
            session.add(task_log)
            session.commit()

    def schedule_retry(
        self,
        service_name: str,
        service_method: str,
        args: list,
        kwargs: dict,
        attempts: int,
        max_attempts: int,
    ):
        redis_client.lpush(
            "task_queue",
            json.dumps(
                {
                    "service_name": service_name,
                    "service_method": service_method,
                    "args": args,
                    "kwargs": kwargs,
                    "attempts": attempts,
                    "max_attempts": max_attempts,
                }
            ),
        )
