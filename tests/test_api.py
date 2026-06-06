import time
from unittest.mock import patch

import pytest
from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root_endpoint(ac: AsyncClient):
    response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": "operational",
        "service": "circuit-breaker-manager",
    }


@pytest.mark.asyncio
async def test_register_service(ac: AsyncClient):
    unique_suffix = int(time.time())

    payload = {
        "name": f"auth_service_{unique_suffix}",
        "url": "http://localhost:9000/health",
        "ping_interval": 5,
    }

    response = await ac.post("/services/register-service", json=payload)

    assert response.status_code in [
        200,
        201,
    ], f"Бекенд повернув 400. Опис помилки: {response.text}"

    data = response.json()

    assert "id" in data
    assert data["name"] == f"auth_service_{unique_suffix}"


@pytest.mark.asyncio
async def test_register_service_exception(ac: AsyncClient):
    payload = {
        "name": "faulty_service",
        "url": "http://localhost/health",
        "ping_interval": 1,
    }

    with patch(
        "app.crud.service.create_service",
        side_effect=Exception("Database crash simulator"),
    ):
        response = await ac.post("/services/register-service", json=payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "cant register new service" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_health_microservice(ac: AsyncClient):
    unique_suffix = int(time.time()) + 1
    payload = {
        "name": f"health_check_service_{unique_suffix}",
        "url": "http://localhost:9001/health",
        "ping_interval": 5,
    }
    reg_response = await ac.post("/services/register-service", json=payload)
    service_id = reg_response.json()["id"]

    response = await ac.get(f"/services/health/{service_id}")
    assert response.status_code in [
        200,
        201,
    ], f"Бекенд повернув 400. Опис помилки: {response.text}"
    assert response.json()["id"] == service_id


@pytest.mark.asyncio
async def test_get_health_fake_microservice(ac: AsyncClient):
    fake_id = 9999999
    response = await ac.get(f"/services/health/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "service not found"


def test_websocket(ws_client):
    with ws_client.websocket_connect("/ws/status") as websocket:
        payload_text = "ping_from_test"
        websocket.send_text(payload_text)

        data = websocket.receive_json()

        assert data["event"] == "pong"
        assert data["client_data"] == "ping_from_test"


@pytest.mark.asyncio
async def test_get_metrics(ac: AsyncClient):
    response = await ac.get("/metrics")
    assert response.status_code == 200

    assert "text/plain" in response.headers["content-type"]

    assert 'health_checks_total{status="success"} 0' in response.text
    assert 'health_checks_total{status="failure"} 0' in response.text
    assert "health_check_avg_response_time_seconds 0.0000" in response.text

    assert "# HELP health_checks_total" in response.text
    assert "# TYPE health_checks_total counter" in response.text
    assert "# HELP health_check_avg_response_time_seconds" in response.text
    assert "# TYPE health_check_avg_response_time_seconds gauge" in response.text


@pytest.mark.asyncio
async def test_manual_trip_not_found(ac: AsyncClient):
    response = await ac.post("/services/circuit_breaker/888888/trip")
    assert response.status_code == 404
    assert response.json()["detail"] == "service not found"


@pytest.mark.asyncio
async def test_manual_trip_service_success(ac: AsyncClient):
    unique_suffix = int(time.time()) + 2
    payload = {
        "name": f"trip_service_{unique_suffix}",
        "url": "http://localhost:9002/health",
        "ping_interval": 5,
    }

    reg_response = await ac.post("/services/register-service", json=payload)
    assert reg_response.status_code in [200, 201]
    service_id = reg_response.json()["id"]

    trip_response = await ac.post(f"/services/circuit_breaker/{service_id}/trip")
    assert trip_response.status_code == 200

    data = trip_response.json()
    assert data["service_id"] == service_id
    assert data["to_state"] == "OPEN"
    assert "manual trip by administrator" in data["reason"]
