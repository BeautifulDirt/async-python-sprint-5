from http import HTTPStatus

from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_ping():
    response = client.get('/ping')
    assert response.status_code == HTTPStatus.OK
    result = response.json()
    assert len(result) == 2


def test_list_file():
    response = client.get('/files/list')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    result = response.json()
    assert len(result) == 1
    assert result.get("detail") == "Unauthorized"


def test_files_upload():
    response = client.get('/files/upload')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    result = response.json()
    assert len(result) == 1
    assert result.get("detail") == "Unauthorized"


def test_files_download():
    response = client.get('/files/download')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    result = response.json()
    assert len(result) == 1
    assert result.get("detail") == "Unauthorized"
