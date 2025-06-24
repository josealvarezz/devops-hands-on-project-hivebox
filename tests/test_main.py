from datetime import datetime, timezone, timedelta
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app, __version__
import requests

client = TestClient(app)


def test_get_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": __version__}


def make_mock_response(temp=None, date=None, corrupt=False):
    class MockResponse:
        def json(self):
            if corrupt:
                return {
                    "sensors": [
                        {}, {},
                        {
                            "lastMeasurement": {
                                # Value is missing
                            }
                        }
                    ]
                }
            else:
                return {
                    "sensors": [
                        {}, {},
                        {
                            "lastMeasurement": {
                                "value": temp,
                                "createdAt": date
                            }
                        }
                    ]
                }
    return MockResponse()


def mock_requests_get_happy(*args, **kwargs):
    now = datetime.now(timezone.utc)
    recent_time = (now - timedelta(minutes=10)
                   ).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return make_mock_response(22.5, recent_time)


@patch("app.sensebox.requests.get", side_effect=mock_requests_get_happy)
def test_temperature_happy_path(mock_get):
    response = client.get("/temperature")
    assert response.status_code == 200
    assert "temperature" in response.json()


def mock_requests_get_old(*args, **kwargs):
    now = datetime.now(timezone.utc)
    old_time = (now - timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    return make_mock_response(22.5, old_time)


@patch("app.sensebox.requests.get", side_effect=mock_requests_get_old)
def test_temperature_old(mock_get):
    response = client.get("/temperature")
    assert response.status_code == 404
    assert response.json()["detail"] == "No recent temperature data available"


def mock_requests_get_mixed(*args, **kwargs):
    url = args[0]
    now = datetime.now(timezone.utc)
    recent_time = (now - timedelta(minutes=10)
                   ).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    old_time = (now - timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    if "5c72ec079e6756001987288b" in url:
        return make_mock_response(20, recent_time)
    elif "61eec6bf848248001ba4beeb" in url:
        return make_mock_response(25, old_time)
    elif "61bf38bf19a991001b0e5cb4" in url:
        return make_mock_response(22, recent_time)
    else:
        return make_mock_response(0, recent_time)


@patch("app.sensebox.requests.get", side_effect=mock_requests_get_mixed)
def test_temperature_some_valid_some_old(mock_get):
    response = client.get("/temperature")
    assert response.status_code == 200
    expected_average = round((20 + 22) / 2, 2)
    assert response.json()["temperature"] == expected_average


def mock_requests_get_corrupt(*args, **kwargs):
    url = args[0]
    now = datetime.now(timezone.utc)
    recent_time = (now - timedelta(minutes=10)
                   ).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    if "5c72ec079e6756001987288b" in url:
        return make_mock_response(corrupt=True)
    elif "61eec6bf848248001ba4beeb" in url:
        return make_mock_response(25, recent_time)
    elif "61bf38bf19a991001b0e5cb4" in url:
        return make_mock_response(20, recent_time)
    else:
        return make_mock_response(0, recent_time)


@patch("app.sensebox.requests.get", side_effect=mock_requests_get_corrupt)
def test_temperature_some_corrupt(mock_get):
    response = client.get("/temperature")
    assert response.status_code == 200
    expected_average = round((25 + 20) / 2, 2)
    assert response.json()["temperature"] == expected_average


def mock_requests_get_all_corrupt(*args, **kwargs):
    return make_mock_response(corrupt=True)


@patch("app.sensebox.requests.get", side_effect=mock_requests_get_all_corrupt)
def test_temperature_all_corrupt(mock_get):
    response = client.get("/temperature")
    assert response.status_code == 404
    assert response.json()["detail"] == "No recent temperature data available"


@patch("app.sensebox.requests.get", side_effect=requests.exceptions.RequestException("API unreachable"))
def test_temperature_api_error(mock_get):
    response = client.get("/temperature")
    assert response.status_code == 502
    assert response.json()["detail"] == "Error fetching data from openSenseMap"


def mock_requests_get_extremes(*args, **kwargs):
    url = args[0]
    now = datetime.now(timezone.utc)
    recent_time = (now - timedelta(minutes=5)
                   ).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    if "5c72ec079e6756001987288b" in url:
        return make_mock_response(-50, recent_time)
    elif "61eec6bf848248001ba4beeb" in url:
        return make_mock_response(100, recent_time)
    elif "61bf38bf19a991001b0e5cb4" in url:
        return make_mock_response(9999, recent_time)
    else:
        return make_mock_response(0, recent_time)


@patch("app.sensebox.requests.get", side_effect=mock_requests_get_extremes)
def test_temperature_extreme_values(mock_get):
    response = client.get("/temperature")
    assert response.status_code == 200
    expected_average = round((-50 + 100 + 9999) / 3, 2)
    assert response.json()["temperature"] == expected_average
