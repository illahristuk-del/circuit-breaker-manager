import time
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_service(ac: AsyncClient):
    unique_suffix = int(time.time())

    payload = {
        "name": f"auth_service_{unique_suffix}",
        "url": "http://localhost:9000/health",
        "ping_interval": 5
    }

    response = await ac.post("/services/register-service", json=payload)

    assert response.status_code in [200, 201], f"Бекенд повернув 400. Опис помилки: {response.text}"

    data = response.json()

    assert "id" in data
    assert data["name"] == f"auth_service_{unique_suffix}"

@pytest.mark.asyncio
async def test_get_health_fake_microservice(ac: AsyncClient):
    fake_id = 9999999
    response = await ac.get(f"/services/health/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "service not found"
    
@pytest.mark.asyncio
async def test_get_health_microservice(ac: AsyncClient):
    id = 1
    response = await ac.get(f"/services/health/{id}")
    assert response.status_code in [200, 201], f"Бекенд повернув 400. Опис помилки: {response.text}"

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
    assert 'health_check_avg_response_time_seconds 0.0000' in response.text 

    assert "# HELP health_checks_total" in response.text
    assert "# TYPE health_checks_total counter" in response.text
    assert "# HELP health_check_avg_response_time_seconds" in response.text
    assert "# TYPE health_check_avg_response_time_seconds gauge" in response.text