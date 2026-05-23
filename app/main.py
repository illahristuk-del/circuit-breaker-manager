from fastapi import FastAPI
from app.routers.service import router as service_router
from app.routers.metrics import router as metrics_router
from app.routers.websocket import router as ws_router

app = FastAPI(
    title="FinTech Circuit Breaker Manager",
    description="Критично важливий мікросервіс моніторингу зовнішніх API платіжних систем",
    version="1.0.0"
)

app.include_router(service_router)
app.include_router(metrics_router)
app.include_router(ws_router)

@app.get("/")
async def root() -> dict[str, str]:
    return {"status": "operational", "service": "circuit-breaker-manager"}