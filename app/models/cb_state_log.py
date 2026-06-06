from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.models.service import TaskStatus


class CircuitBreakerStateLog(Base):
    __tablename__ = "circuit_breaker_state_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id", ondelete="CASCADE"), nullable=False
    )

    from_state: Mapped[TaskStatus] = mapped_column(SQLEnum(TaskStatus), nullable=False)
    to_state: Mapped[TaskStatus] = mapped_column(SQLEnum(TaskStatus), nullable=False)

    reason: Mapped[str] = mapped_column(String(500), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
