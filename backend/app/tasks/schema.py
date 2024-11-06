import datetime
from typing import Optional
from pydantic import BaseModel, Field
from .models import TaskStatus


class TaskInput(BaseModel):  # type: ignore
    title: str = Field(min_length=1, max_length=50)
    description: str | None = None
    user_id: int | None = None
    due_date: datetime.datetime | None = None
    status: TaskStatus = TaskStatus.created


class TaskOutput(BaseModel):  # type: ignore
    id: int
    title: str
    description: Optional[str] = ""
    user_id: int
    due_date: datetime.datetime | None = None
    status: TaskStatus
