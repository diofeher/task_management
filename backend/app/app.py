from fastapi import FastAPI
from contextlib import asynccontextmanager

from .routers import task, user
from .db import create_db_and_tables

from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
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
