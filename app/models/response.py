from pydantic import BaseModel
from typing import List
from datetime import date


class ForecastDay(BaseModel):
    date: date
    weather_code: int
    temp_min: float
    temp_max: float
    energy: float


class ForecastResponse(BaseModel):
    forecast: List[ForecastDay]


class SummaryResponse(BaseModel):
    avg_pressure: float
    avg_sun_hours: float
    temp_min: float
    temp_max: float
    is_rainy_week: bool 

