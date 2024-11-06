from datetime import datetime
import enum
from sqlmodel import Field, SQLModel, Enum, Column
from pydantic import ConfigDict


class TaskStatus(str, enum.Enum):
    started = "started"
    deleted = "deleted"
    finished = "finished"
    created = "created"


class TaskBase(SQLModel):  # type: ignore
    title: str
    description: str | None
    due_date: datetime | None = Field(nullable=True, default=None)
    status: TaskStatus = Field(
        sa_column=Column(Enum(TaskStatus)), default=TaskStatus.created
    )
    user_id: int | None = Field(default=None, foreign_key="user.id")


class Task(TaskBase, table=True):
    model_config = ConfigDict(validate_assignment=True)  # type: ignore

    id: int | None = Field(default=None, primary_key=True, index=True)
