from typing import AsyncGenerator
from .tasks.routers import router as task_router
from .users.routers import router as user_router
from fastapi import FastAPI
from contextlib import asynccontextmanager

from .db import create_db_and_tables

from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    # Load the ML model
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(task_router)
app.include_router(user_router)

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
