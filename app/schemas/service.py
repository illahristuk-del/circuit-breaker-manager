from pydantic import BaseModel, Field, HttpUrl
from typing import Annotated
from datetime import datetime
from app.models.service import TaskStatus

class ServiceBase(BaseModel):
    name: Annotated[str, Field(max_length=225)]
    url: HttpUrl

class CreateService(ServiceBase):
    pass

class ResponseService(ServiceBase):
    id: int
    status: TaskStatus

    model_config = {"from_attributes": True}

class ResponseHealthCheckLog(BaseModel):
    id: int
    service_id: int
    is_alive: bool
    status_code: int | None
    response_time: float = Field(description="response time in seconds")
    error_message: str | None
    created_at: datetime

    model_config = {"from_attributes": True}

class ResponseCBStateResponse(BaseModel):
    id: int
    service_id: int
    from_state: TaskStatus
    to_state: TaskStatus
    reason: str = Field(max_length=500)
    created_at: datetime

    model_config = {"from_attributes": True}