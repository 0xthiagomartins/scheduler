def test_schedule_task(scheduler_service):
    response = scheduler_service.schedule_task(
        "* * * * *", "test_service", "test_method", [], {}, 3
    )
    assert (
        response["message"] == "Scheduled test_service.test_method with cron * * * * *"
    )
