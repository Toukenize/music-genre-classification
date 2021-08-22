from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from src.config import settings
from src.main import app


def test_predict_batch_standard_file():
    url = f"{settings.API_PREFIX}/predict-batch"

    test_file_path = Path('tests', 'test_files', 'test.csv')
    test_file = {'csv_file': test_file_path.open('rb')}
    with TestClient(app) as client:
        response = client.post(
            url,
            files=test_file,
            headers={
                'client-id': settings.CLIENT_ID,
                'client-secret': settings.CLIENT_SECRET,
            }
        )

        assert response.json() == {
            "status": "success",
            "status_code": 200,
            "info": {
                "total_rows_uploaded": 428,
                "total_rows_w_na": 0,
                "total_rows_added_to_db": 428
            }
        }


def test_predict_batch_auth():
    url = f"{settings.API_PREFIX}/predict-batch"

    test_file_path = Path('tests', 'test_files', 'test.csv')
    test_file = {'csv_file': test_file_path.open('rb')}

    with TestClient(app) as client:
        response = client.post(
            url,
            files=test_file,
            headers={
                'client-id': 'zxc',
                'client-secret': 'asd',
            }
        )

    assert response.status_code == 401


@pytest.mark.skip(
    reason="""
    Unable to test bare exception.
    Context : By right this should raise a DataSchemaException,
    but due to some Starlette bug
    (https://github.com/tiangolo/fastapi/issues/2683#issuecomment-764000404)
    it is raising a general Exception,
    which is not testable on FastAPI
    (https://github.com/tiangolo/fastapi/issues/2799)
    """
)
def test_predict_batch_missing_col():
    url = f"{settings.API_PREFIX}/predict-batch"

    test_file_path = Path('tests', 'test_files', 'test_bad_missing_col.csv')
    test_file = {'csv_file': test_file_path.open('rb')}

    with TestClient(app) as client:
        response = client.post(
            url,
            files=test_file,
            headers={
                'client-id': settings.CLIENT_ID,
                'client-secret': settings.CLIENT_SECRET,
            }
        )
    assert response.status_code == 500


@pytest.mark.skip(
    reason="""
    Unable to test bare exception.
    Context : By right this should raise a DataSchemaException,
    but due to some Starlette bug
    (https://github.com/tiangolo/fastapi/issues/2683#issuecomment-764000404)
    it is raising a general Exception,
    which is not testable on FastAPI
    (https://github.com/tiangolo/fastapi/issues/2799)
    """
)
def test_predict_batch_wrong_cell_type():
    url = f"{settings.API_PREFIX}/predict-batch"

    test_file_path = Path('tests', 'test_files',
                          'test_bad_wrong_cell_type.csv')
    test_file = {'csv_file': test_file_path.open('rb')}

    with TestClient(app) as client:
        response = client.post(
            url,
            files=test_file,
            headers={
                'client-id': settings.CLIENT_ID,
                'client-secret': settings.CLIENT_SECRET,
            }
        )
    assert response.status_code == 500
