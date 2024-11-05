from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from dataclasses import dataclass
from .models import Task, TaskStatus
from .schema import TaskInput, TaskOutput


@dataclass
class TaskRepository:
    session: Session
    current_user_id: int

    def create(self, data: TaskInput) -> TaskOutput:
        task = Task(**data.model_dump(exclude_none=True))
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return TaskOutput(**dict(task))

    def list(self, offset: int, limit: int) -> List[Optional[TaskOutput]]:
        stmt = (
            select(Task)
            .where(
                Task.status != TaskStatus.deleted,
                Task.user_id == self.current_user_id,
            )
            .offset(offset)
            .limit(limit)
        )
        tasks = self.session.execute(stmt).all()
        return [TaskOutput(**dict(task[0])) for task in tasks]

    def get_by_id(self, id: int) -> Task:
        return self.session.get(Task, id)

    def update(self, task: Task) -> TaskOutput:
        self.session.execute(
            update(Task).where(Task.id == task.id).values(**dict(task))
        )
        self.session.commit()
        self.session.refresh(task)
        return TaskOutput(**dict(task))
