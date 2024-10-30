from fastapi import FastAPI
from app.models import (
    create_db_and_tables,
    engine,
)

from .routers import task, user

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(task.router)
app.include_router(user.router)

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


@app.on_event("startup")
def on_startup():
    create_db_and_tables(engine)
