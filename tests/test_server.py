import pytest
pytestmark = pytest.mark.server

def test_server_health():
    from fastapi.testclient import TestClient
    from caereflex.server.app import create_app
    client = TestClient(create_app())
    r = client.get('/health')
    assert r.status_code == 200
    assert r.json()['status'] == 'success'

def test_openapi():
    from fastapi.testclient import TestClient
    from caereflex.server.app import create_app
    client = TestClient(create_app())
    assert client.get('/openapi.json').status_code == 200
    assert client.get('/openapi.yaml').status_code == 200
