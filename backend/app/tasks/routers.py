from typing import Annotated
from fastapi import Depends, Query, APIRouter
from sqlalchemy.orm import Session
from app.users.models import User
from app.auth import get_current_active_user
from app.db import get_session
from .schema import TaskInput, TaskOutput
from .service import TaskService


router = APIRouter(prefix="/tasks")


@router.get("/")
def read_tasks(
    *,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    return TaskService(session, current_user.id).list(offset, limit)


@router.post("/", response_model=TaskOutput)
def create_task(
    *,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session),
    data: TaskInput,
):
    return TaskService(session, current_user.id).create(data)


@router.get("/{task_id}")
def read_task(
    *,
    session: Session = Depends(get_session),
    current_user: Annotated[User, Depends(get_current_active_user)],
    task_id: int,
):
    return TaskService(session, current_user.id).read(task_id)


@router.patch("/{task_id}")
def update_task(
    *,
    session: Session = Depends(get_session),
    current_user: Annotated[User, Depends(get_current_active_user)],
    task_id: int,
    task: TaskInput,
):
    return TaskService(session, current_user.id).update(task_id, task)


@router.delete("/{task_id}")
def delete_task(
    *,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session),
    task_id: int,
):
    return TaskService(session, current_user.id).delete(task_id)
