# TODO: Move to its own module
from sqlmodel import Session, select

from fastapi import Depends, FastAPI, Query, HTTPException
from src.models import (
    Task,
    TaskUpdate,
    TaskCreate,
    TaskStatus,
    create_db_and_tables,
    engine,
    get_session,
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# TODO: Move to another file
@app.on_event("startup")
def on_startup():
    create_db_and_tables(engine)


@app.get("/tasks/")
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


@app.post("/tasks/")
def create_task(*, session: Session = Depends(get_session), task: TaskCreate):
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@app.get("/tasks/{task_id}")
def read_task(*, session: Session = Depends(get_session), task_id: int):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.patch("/tasks/{task_id}")
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


@app.delete("/tasks/{task_id}")
def delete_task(*, session: Session = Depends(get_session), task_id: int):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db_task.status = TaskStatus.deleted
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
