from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import Annotated

from app.database import get_db
from app.models.health_log import HealthCheckLog

router = APIRouter(tags=["Metrics"])

DB_DEPENDS = Annotated[AsyncSession, Depends(get_db)]

@router.get("/metrics")
async def get_prometheus_metrics(db: DB_DEPENDS):
    query_counts = await db.execute(
        select(HealthCheckLog.is_alive, func.count(HealthCheckLog.id))
        .group_by(HealthCheckLog.is_alive)
    )
    counts = dict(query_counts.all())
    
    success_count = counts.get(True, 0)
    failure_count = counts.get(False, 0)

    query_avg_time = await db.execute(select(func.avg(HealthCheckLog.response_time)))
    avg_response_time = query_avg_time.scalar() or 0.0

    prometheus_data = (
        f"# HELP health_checks_total Total number of health checks performed.\n"
        f"# TYPE health_checks_total counter\n"
        f'health_checks_total{{status="success"}} {success_count}\n'
        f'health_checks_total{{status="failure"}} {failure_count}\n\n'
        f"# HELP health_check_avg_response_time_seconds Average response time of external services.\n"
        f"# TYPE health_check_avg_response_time_seconds gauge\n"
        f"health_check_avg_response_time_seconds {avg_response_time:.4f}\n"
    )

    return Response(content=prometheus_data, media_type="text/plain")