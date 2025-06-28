import pytest
from unittest.mock import patch, MagicMock
from app.services.weather import get_summary_data
from app.models.request import ForecastRequestParams


@pytest.mark.asyncio
@patch("app.services.weather.httpx.AsyncClient.get")
async def test_summary_correct_aggregation(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {
        "daily": {
            "time": ["2025-06-28", "2025-06-29"],
            "temperature_2m_min": [12.0, 10.0],
            "temperature_2m_max": [25.0, 28.0],
            "sunshine_duration": [36000, 18000],  # seconds
            "weathercode": [1, 2]
        },
        "hourly": {
            "time": [
                "2025-06-28T00:00", "2025-06-28T01:00",
                "2025-06-29T00:00", "2025-06-29T01:00"
            ],
            "surface_pressure": [1000.0, 1002.0, 1005.0, 1003.0]
        }
    }
    mock_get.return_value = mock_response

    params = ForecastRequestParams(lat=50.0, lon=20.0)
    summary = await get_summary_data(params)

    assert summary.temp_min == 10.0
    assert summary.temp_max == 28.0
    assert round(summary.avg_pressure, 2) == 1002.5
    assert round(summary.avg_sun_hours, 2) == 7.5  # (10 + 5) h avg
    assert summary.is_cloudy_week is False


@pytest.mark.asyncio
@patch("app.services.weather.httpx.AsyncClient.get")
async def test_summary_detects_rainy_week(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {
        "daily": {
            "time": ["2025-06-28", "2025-06-29", "2025-06-30", "2025-07-01"],
            "temperature_2m_min": [10.0, 11.0, 12.0, 13.0],
            "temperature_2m_max": [20.0, 21.0, 22.0, 23.0],
            "sunshine_duration": [10000, 20000, 30000, 40000],
            "weathercode": [51, 53, 61, 63]  # deszczowe kody (≥50)
        },
        "hourly": {
            "time": [f"2025-06-28T0{i}:00" for i in range(4)],
            "surface_pressure": [990.0, 991.0, 992.0, 993.0]
        }
    }
    mock_get.return_value = mock_response

    params = ForecastRequestParams(lat=50.0, lon=20.0)
    summary = await get_summary_data(params)

    assert summary.is_cloudy_week is True
