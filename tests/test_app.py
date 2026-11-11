"""Unit tests for the HTTP service."""

import uuid
import pytest
from freezegun import freeze_time

from app.main import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_returns_200_and_json(client):
    response = client.get("/acc-123/data")

    assert response.status_code == 200
    assert response.is_json


def test_response_has_the_expected_fields(client):
    body = client.get("/acc-123/data").get_json()

    assert set(body.keys()) == {"accountId", "timestamp", "data"}


def test_account_id_is_taken_from_the_path(client):
    body = client.get("/some-account/data").get_json()

    assert body["accountId"] == "some-account"


@freeze_time("2026-11-11 13:34:00")
def test_timestamp_is_current_utc_time_in_iso_format(client):
    body = client.get("/acc-123/data").get_json()

    assert body["timestamp"] == "2026-11-11T13:34:00Z"


def test_data_is_a_random_uuid(client):
    body = client.get("/acc-123/data").get_json()

    assert uuid.UUID(body["data"]).version == 4


def test_data_is_different_on_each_request(client):
    first = client.get("/acc-123/data").get_json()["data"]
    second = client.get("/acc-123/data").get_json()["data"]

    assert first != second


def test_unknown_route_returns_404(client):
    assert client.get("/acc-123").status_code == 404
    assert client.get("/acc-123/other").status_code == 404


def test_only_get_is_allowed(client):
    assert client.post("/acc-123/data").status_code == 405