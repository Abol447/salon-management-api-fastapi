from tests.conftest import client
from fastapi.testclient import TestClient


def test_log_in(client: TestClient):
    res = client.post(
        "/auth/login", json={"phone_number": "09015524448", "password": "123"}
    )
    assert res.status_code == 200
