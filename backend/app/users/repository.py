from dataclasses import dataclass
from sqlalchemy.orm import Session


@dataclass
class UserRepository:
    session: Session
