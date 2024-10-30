from fastapi import Depends, Query, HTTPException, APIRouter
from sqlmodel import Session, select
from app.models import (
    Task,
    TaskUpdate,
    TaskCreate,
    TaskStatus,
    get_session,
)

router = APIRouter()


@router.get("/tasks/")
def read_tasks(
    *,
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


@router.post("/tasks/")
def create_task(*, session: Session = Depends(get_session), task: TaskCreate):
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.get("/tasks/{task_id}")
def read_task(*, session: Session = Depends(get_session), task_id: int):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.patch("/tasks/{task_id}")
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


@router.delete("/tasks/{task_id}")
def delete_task(*, session: Session = Depends(get_session), task_id: int):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db_task.status = TaskStatus.deleted
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
