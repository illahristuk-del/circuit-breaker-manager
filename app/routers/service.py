from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import service as service_crud
from app.database import get_db
from app.models.service import TaskStatus
from app.schemas.service import (
    CreateService,
    ResponseCBStateResponse,
    ResponseService,
)

router = APIRouter(prefix="/services", tags=["Services"])

DB_DEPENDS = Annotated[AsyncSession, Depends(get_db)]


@router.post(
    "/register-service",
    response_model=ResponseService,
    status_code=status.HTTP_201_CREATED,
)
async def register_service(service_data: CreateService, db: DB_DEPENDS):
    try:
        new_service = await service_crud.create_service(
            db=db, service_data=service_data
        )
        return new_service
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"cant register new service, try again\nerror: {str(e)}",
        )


@router.post(
    "/circuit_breaker/{service_id}/trip", response_model=ResponseCBStateResponse
)
async def manual_trip_service(service_id: int, db: DB_DEPENDS):
    service = await service_crud.get_service_by_db(db=db, service_id=service_id)
    if service is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="service not found"
        )

    old_state = service.status
    service.status = TaskStatus.OPEN

    state_log = await service_crud.create_cb_state_log(
        db=db,
        service_id=service_id,
        from_state=old_state,
        to_state=TaskStatus.OPEN,
        reason="manual trip by administrator",
    )

    return state_log


@router.get("/health/{service_id}", response_model=ResponseService)
async def get_service_health(service_id: int, db: DB_DEPENDS):
    service = await service_crud.get_service_by_db(db=db, service_id=service_id)
    if service is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="service not found"
        )
    return service
