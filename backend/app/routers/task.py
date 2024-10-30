from typing import Annotated
from fastapi import Depends, Query, HTTPException, APIRouter
from sqlmodel import Session, select
from app.models.user import User
from app.auth import get_current_active_user
from app.models.task import (
    Task,
    TaskUpdate,
    TaskCreate,
    TaskStatus,
)

from app.models import get_session

router = APIRouter(prefix="/tasks")


@router.get("/")
def read_tasks(
    *,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    stmt = (
        select(Task)
        .where(Task.status != TaskStatus.deleted)
        .offset(offset)
        .limit(limit)
    )
    tasks = session.exec(stmt).all()
    return tasks


@router.post("/")
def create_task(*, session: Session = Depends(get_session), task: TaskCreate):
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.get("/{task_id}")
def read_task(*, session: Session = Depends(get_session), task_id: int):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.patch("/{task_id}")
def update_task(
    *, session: Session = Depends(get_session), task_id: int, task: TaskUpdate
):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = task.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(task_data)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.delete("/{task_id}")
def delete_task(*, session: Session = Depends(get_session), task_id: int):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db_task.status = TaskStatus.deleted
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task