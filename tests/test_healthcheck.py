from fastapi.testclient import TestClient
from src.config import settings
from src.main import app


def test_healthcheck():
    client = TestClient(app)
    url = f"{settings.API_PREFIX}/healthcheck"
    response = client.get(url)

    assert response.status_code == 200
    j = response.json()

    assert j == {
        "status": "success",
        "version": settings.API_VERSION,
        "name": settings.API_NAME
    }
