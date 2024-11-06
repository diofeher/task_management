from typing import List
from sqlalchemy.orm import Session
from dataclasses import dataclass
from fastapi import HTTPException
from .repository import TaskRepository
from .models import TaskStatus, Task
from .schema import TaskInput, TaskOutput


@dataclass
class TaskService:
    session: Session
    current_user_id: int | None

    def __post_init__(self) -> None:
        self.repository: TaskRepository = TaskRepository(
            self.session, self.current_user_id
        )

    def get_or_not_found(self, task_id: int) -> Task:
        task = self.repository.get_by_id(task_id)
        if (not task) or (task.user_id != self.current_user_id):
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    def list(self, offset: int, limit: int) -> List[TaskOutput]:
        return self.repository.list(offset, limit)

    def create(self, data: TaskInput) -> TaskOutput:
        data.user_id = self.current_user_id
        return self.repository.create(data)

    def read(self, task_id: int) -> TaskOutput:
        task = self.get_or_not_found(task_id)
        return TaskOutput(**dict(task))

    def update(self, task_id: int, data: TaskInput) -> TaskOutput:
        task = self.get_or_not_found(task_id)
        task.title = data.title
        task.description = data.description
        task.due_date = data.due_date

        task.user_id = self.current_user_id
        self.repository.update(task)
        return TaskOutput(**dict(task))

    def delete(self, task_id: int) -> TaskOutput:
        task = self.get_or_not_found(task_id)

        task.status = TaskStatus.deleted
        self.repository.update(task)
        return TaskOutput(**dict(task))
