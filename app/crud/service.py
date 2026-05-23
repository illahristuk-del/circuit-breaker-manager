from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.service import Service, TaskStatus
from app.models.health_log import HealthCheckLog
from app.models.cb_state_log import CircuitBreakerStateLog
from app.schemas.service import CreateService
from fastapi import HTTPException

async def create_service(db: AsyncSession, service_data: CreateService) -> Service:
    db_service = Service(**service_data.model_dump(mode="json"))

    db.add(db_service)
    await db.commit()
    await db.refresh(db_service)
    return db_service

async def get_service_by_db(db: AsyncSession, service_id: int) -> Service | None:
    result = await db.execute(select(Service).where(Service.id == service_id))
    return result.scalar_one_or_none()

async def get_all_services_by_db(db: AsyncSession) -> list[Service]:
    result = await db.execute(select(Service))
    return list[result.scalars().all()]

async def create_health_log(db: AsyncSession, 
    service_id: int, 
    is_alive: bool, 
    status_code: int | None, 
    response_time: float, 
    error_message: str | None = None
    ) -> HealthCheckLog:
    
    get_service = await db.execute(select(Service).where(Service.id == service_id))
    service = get_service.scalar_one_or_none()
    if service is None:
        return None
    
    db_log = HealthCheckLog(
        service_id=service_id,
        is_alive=is_alive,
        status_code=status_code,
        response_time=response_time,
        error_message=error_message,
    )

    db.add(db_log)
    await db.commit()
    await db.refresh(db_log)
    return db_log

async def create_cb_state_log(db: AsyncSession,
    service_id: int,
    from_state: TaskStatus,
    to_state: TaskStatus,
    reason: str
    ) -> CircuitBreakerStateLog:

    get_service = await db.execute(select(Service).where(Service.id == service_id))
    service = get_service.scalar_one_or_none()
    
    if service is None:
        return None

    db_state_log = CircuitBreakerStateLog(
        service_id=service_id,
        from_state=from_state,
        to_state=to_state,
        reason=reason
    )

    db.add(db_state_log)
    await db.commit()
    await db.refresh(db_state_log)
    return db_state_log