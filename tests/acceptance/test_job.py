import time

import mock
import pytest

pytestmark = [pytest.mark.acceptance, pytest.mark.api, pytest.mark.jobs]


def test_it_gets_jobs(api_client, jobs_endpoint, job_factory, stack):
    # Arrange
    job_id = job_factory()["JobId"]
    # Act
    response = api_client.get("{}/{}".format(jobs_endpoint, job_id))
    response_body = response.json()
    # Assert
    assert response.status_code == 200
    assert {
        "JobId": job_id,
        "JobStatus": mock.ANY,
        "GSIBucket": mock.ANY,
        "CreatedAt": mock.ANY,
    } == response_body
    assert response.headers.get("Access-Control-Allow-Origin") == stack["APIAccessControlAllowOriginHeader"]


def test_it_handles_unknown_jobs(api_client, jobs_endpoint, stack):
    # Arrange
    job_id = "invalid"
    # Act
    response = api_client.get("{}/{}".format(jobs_endpoint, job_id))
    # Assert
    assert response.status_code == 404
    assert response.headers.get("Access-Control-Allow-Origin") == stack["APIAccessControlAllowOriginHeader"]


def test_it_lists_jobs_by_date(api_client, jobs_endpoint, job_factory, stack):
    # Arrange
    job_id_1 = job_factory(job_id="123", created_at=1576861489)["JobId"]
    job_id_2 = job_factory(job_id="234", created_at=1576861490)["JobId"]
    time.sleep(1)  # No item waiter therefore wait for gsi propagation
    # Act
    response = api_client.get(jobs_endpoint)
    response_body = response.json()
    # Assert
    assert response.status_code == 200
    assert {
        "JobId": job_id_2,
        "JobStatus": mock.ANY,
        "GSIBucket": mock.ANY,
        "CreatedAt": mock.ANY,
    } == response_body["Jobs"][0]
    assert {
        "JobId": job_id_1,
        "JobStatus": mock.ANY,
        "GSIBucket": mock.ANY,
        "CreatedAt": mock.ANY,
    } == response_body["Jobs"][1]
    assert response.headers.get("Access-Control-Allow-Origin") == stack["APIAccessControlAllowOriginHeader"]
