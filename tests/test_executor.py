def test_execute_task_success(scheduler_service, mocker):
    mock_proxy = mocker.patch("src.business.executor.RpcProxy")
    mock_method = mocker.Mock()
    mock_method.return_value = None
    mock_proxy.return_value.test_service.test_method = mock_method
    scheduler_service.execute_task("test_service", "test_method", [], {}, 0, 3)
    logs = scheduler_service.get_task_logs()
    assert logs[-1].status == "success"


def test_execute_task_failure(scheduler_service, mocker):
    mock_proxy = mocker.patch("src.business.executor.RpcProxy")
    mock_method = mocker.Mock()
    mock_method.side_effect = Exception("Test Exception")
    mock_proxy.return_value.test_service.test_method = mock_method
    scheduler_service.execute_task("test_service", "test_method", [], {}, 0, 3)
    logs = scheduler_service.get_task_logs()
    assert logs[-1].status == "failed"
