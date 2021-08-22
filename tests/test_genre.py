import pytest
from fastapi.testclient import TestClient
from src.config import settings
from src.genre.schema.input_data import Genre
from src.main import app

genres = list(genre.value for genre in Genre)


@pytest.mark.parametrize('genre', genres)
def test_genre_title_list(genre):
    client = TestClient(app)

    url = f"{settings.API_PREFIX}/genre/title-list"

    response = client.get(
        url,
        params={'genre': genre},
        headers={
            'client-id': settings.CLIENT_ID,
            'client-secret': settings.CLIENT_SECRET,
        }
    )

    assert response.status_code == 200
    assert response.json()['genre'] == genre


def test_genre_list():
    client = TestClient(app)
    url = f"{settings.API_PREFIX}/genre/list"
    response = client.get(
        url,
        headers={
            'client-id': settings.CLIENT_ID,
            'client-secret': settings.CLIENT_SECRET,
        }
    )

    assert response.status_code == 200
