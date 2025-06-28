import pytest
from pydantic import ValidationError
from app.models.request import ForecastRequestParams


def test_valid_model_defaults():
    m = ForecastRequestParams(lat=50.0, lon=20.0)
    assert m.power == 2.5
    assert m.efficiency == 0.2


def test_invalid_latitude():
    with pytest.raises(ValidationError):
        ForecastRequestParams(lat=200.0, lon=20.0)


def test_invalid_longitude():
    with pytest.raises(ValidationError):
        ForecastRequestParams(lat=50.0, lon=300.0)


def test_invalid_efficiency_too_high():
    with pytest.raises(ValidationError):
        ForecastRequestParams(lat=50.0, lon=20.0, efficiency=1.5)


def test_invalid_efficiency_zero():
    with pytest.raises(ValidationError):
        ForecastRequestParams(lat=50.0, lon=20.0, efficiency=0.0)


def test_invalid_power_negative():
    with pytest.raises(ValidationError):
        ForecastRequestParams(lat=50.0, lon=20.0, power=-1)
