from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# === FORECAST ===

def test_forecast_valid_request():
    response = client.get("/forecast", params={
        "lat": 50.0,
        "lon": 20.0
    })
    assert response.status_code == 200
    data = response.json()
    assert "forecast" in data
    assert len(data["forecast"]) == 7
    for day in data["forecast"]:
        assert "date" in day
        assert "weather_code" in day
        assert "temp_min" in day
        assert "temp_max" in day
        assert "energy" in day


def test_forecast_invalid_efficiency():
    response = client.get("/forecast", params={
        "lat": 50.0, "lon": 20.0,
        "efficiency": 1.5  # invalid (>1)
    })
    assert response.status_code == 422


def test_forecast_invalid_power():
    response = client.get("/forecast", params={
        "lat": 50.0, "lon": 20.0,
        "power": -1  # invalid
    })
    assert response.status_code == 422


# === SUMMARY ===

def test_summary_valid_request():
    response = client.get("/summary", params={
        "lat": 50.0,
        "lon": 20.0
    })
    assert response.status_code == 200
    data = response.json()
    assert "avg_pressure" in data
    assert "avg_sun_hours" in data
    assert "temp_min" in data
    assert "temp_max" in data
    assert "is_rainy_week" in data


def test_summary_invalid_lat():
    response = client.get("/summary", params={
        "lat": 200.0,  # invalid
        "lon": 20.0
    })
    assert response.status_code == 422
