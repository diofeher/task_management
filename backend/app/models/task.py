from datetime import datetime
import enum
from sqlmodel import Field, SQLModel, Enum, Column


class TaskStatus(str, enum.Enum):
    started = "started"
    deleted = "deleted"
    finished = "finished"
    created = "created"


class TaskBase(SQLModel):
    title: str
    description: str
    due_date: datetime | None = Field(nullable=True, default=None)
    status: TaskStatus = Field(
        sa_column=Column(Enum(TaskStatus)), default=TaskStatus.created
    )


class Task(TaskBase, table=True):
    class Config:
        validate_assignment = True

    id: int | None = Field(default=None, primary_key=True, index=True)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = Field(
        sa_column=Column(Enum(TaskStatus)), default=TaskStatus.created
    )
