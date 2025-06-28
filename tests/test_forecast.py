from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_forecast_valid_params():
    response = client.get("/forecast", params={
        "lat": 50.06,
        "lon": 19.94,
        "power": 2.5,
        "efficiency": 0.2
    })
    assert response.status_code == 200
    json_data = response.json()
    assert "forecast" in json_data
    assert len(json_data["forecast"]) == 7
    for day in json_data["forecast"]:
        assert "date" in day
        assert "weather_code" in day
        assert "temp_min" in day
        assert "temp_max" in day
        assert "energy" in day


def test_forecast_invalid_efficiency():
    response = client.get("/forecast", params={
        "lat": 50.06,
        "lon": 19.94,
        "power": 2.5,
        "efficiency": 1.5
    })
    assert response.status_code == 422


def test_summary_valid_response():
    response = client.get("/summary", params={
        "lat": 50.06,
        "lon": 19.94
    })
    assert response.status_code == 200
    json_data = response.json()
    assert "avg_pressure" in json_data
    assert "avg_sun_hours" in json_data
    assert "temp_min" in json_data
    assert "temp_max" in json_data
    assert "is_rainy_week" in json_data
