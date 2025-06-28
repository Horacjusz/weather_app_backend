import pytest
from unittest.mock import patch, MagicMock
from app.services.weather import get_forecast_data
from app.models.request import ForecastRequestParams


@pytest.mark.asyncio
@patch("app.services.weather.httpx.AsyncClient.get")
async def test_forecast_energy_calculation(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {
        "daily": {
            "time": ["2025-06-28", "2025-06-29"],
            "weathercode": [1, 2],
            "temperature_2m_max": [25.0, 22.0],
            "temperature_2m_min": [15.0, 12.0],
            "sunshine_duration": [36000, 18000]  # 10h, 5h
        }
    }
    mock_get.return_value = mock_response

    params = ForecastRequestParams(lat=50.0, lon=20.0, power=2.0, efficiency=0.25)
    result = await get_forecast_data(params)

    assert len(result.forecast) == 2
    assert result.forecast[0].energy == 5.0  # 2 * 10 * 0.25
    assert result.forecast[1].energy == 2.5  # 2 * 5 * 0.25


@pytest.mark.asyncio
@patch("app.services.weather.httpx.AsyncClient.get")
async def test_forecast_zero_sun(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {
        "daily": {
            "time": ["2025-06-28"],
            "weathercode": [3],
            "temperature_2m_max": [20.0],
            "temperature_2m_min": [10.0],
            "sunshine_duration": [0]
        }
    }
    mock_get.return_value = mock_response

    params = ForecastRequestParams(lat=50.0, lon=20.0)
    result = await get_forecast_data(params)

    assert len(result.forecast) == 1
    assert result.forecast[0].energy == 0.0
