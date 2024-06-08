import pytest
from nameko.testing.services import worker_factory
from src.service import SchedulerService


@pytest.fixture
def scheduler_service():
    return worker_factory(SchedulerService)
