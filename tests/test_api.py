import pytest
from fastapi.testclient import TestClient
from loguru import logger

from service.configs import settings
from src.service.api import APIProvider


@pytest.fixture(name="client")
def client_fixture():
    app = APIProvider(title=settings.api.name, openapi_url=settings.api.endpoints.prefix + settings.api.openapi_file,
                      docs_url=settings.api.endpoints.prefix + settings.api.docs_path,
                      version=settings.api.version)
    client = TestClient(app.get_api())
    yield client


def test_subtitles(client: TestClient):
    response = client.post(settings.api.endpoints.prefix +
                           '/transcribe',
                           json={"url": 'https://www.youtube.com/watch?v=1aA1WGON49E&ab_channel=TEDxTalks',
                                 "language": None,
                                 "outputDir": "outputs/",
                                 "format": "srt",
                                 "task": "transcribe"},
                           )
    assert response.status_code == 200
    with open('file.srt', 'wb') as s:
        s.write(response.content)


def test_subtitles2(client: TestClient):
    response = client.post(settings.api.endpoints.prefix +
                           '/transcribe',
                           json={"url": 'https://www.youtube.com/watch?v=VuudWT10Oyc&ab_channel=iefimerida.gr',
                                 "language": None,
                                 "outputDir": "outputs/",
                                 "format": "srt",
                                 "task": "translate"},
                           )
    assert response.status_code == 200
    with open('file.srt', 'wb') as s:
        s.write(response.content)


def test_subtitles3(client: TestClient):
    response = client.post(settings.api.endpoints.prefix +
                           '/transcribe',
                           json={"url": 'https://www.youtube.com/watch?v=VuudWT10Oyc&ab_channel=iefimerida.gr',
                                 "language": None,
                                 "outputDir": "outputs/",
                                 "format": "srt",
                                 "task": "transcribe"},
                           )
    assert response.status_code == 200
    with open('file.srt', 'wb') as s:
        s.write(response.content)
