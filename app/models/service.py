from enum import Enum as PyEnum
from sqlalchemy import String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base 

class TaskStatus(str, PyEnum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"

class Service(Base):
    __tablename__ = "services"  

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(225), nullable=False, unique=True)
    url: Mapped[str] = mapped_column(String, nullable=False) 
    status: Mapped[TaskStatus] = mapped_column(SQLEnum(TaskStatus), default=TaskStatus.CLOSED, nullable=False)