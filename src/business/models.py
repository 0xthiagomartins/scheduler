from sqlmodel import SQLModel, Field
from datetime import datetime


class TaskLog(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    task_name: str
    args: str
    kwargs: str
    status: str
    attempts: int
    max_attempts: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
