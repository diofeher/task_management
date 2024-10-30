from typing import Union, Annotated
# TODO: Move to its own module
from sqlmodel import Session, select
from pydantic import AfterValidator
import datetime

from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from src.models import Task, TaskUpdate, TaskCreate, TaskStatus, create_db_and_tables, engine

app = FastAPI()

# TODO: Move to another file
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/tasks/")
def read_tasks(offset: int = 0, limit: int = Query(default=100, le=100)):
    with Session(engine) as session:
        stmt = select(Task).where(Task.status != TaskStatus.deleted).offset(offset).limit(limit)
        tasks = session.exec(stmt).all()
        return tasks
    
@app.post("/tasks/")
def create_task(task: TaskCreate):
    with Session(engine) as session:
        db_task = Task.model_validate(task)
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task

@app.get("/tasks/{task_id}")
def read_task(task_id: int):
    with Session(engine) as session:
        db_task = session.get(Task, task_id)
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        return db_task


@app.patch("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    with Session(engine) as session:
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
def delete_task(task_id: int):
    with Session(engine) as session:
        db_task = session.get(Task, task_id)
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")

        db_task.status = TaskStatus.deleted
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task
