def test_get_task_logs(scheduler_service):
    logs = scheduler_service.get_task_logs()
    assert isinstance(logs, list)


def test_get_task_metrics(scheduler_service):
    metrics = scheduler_service.get_task_metrics()
    assert "total_tasks" in metrics
    assert "success_tasks" in metrics
    assert "failed_tasks" in metrics
