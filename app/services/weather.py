import httpx
from collections import defaultdict
from datetime import date
from app.models.request import ForecastRequestParams
from app.models.response import ForecastDay, ForecastResponse, SummaryResponse

API_URL = "https://api.open-meteo.com/v1/forecast"

async def fetch_weather_data(params: ForecastRequestParams) -> dict:
    query = {
        "latitude": params.lat,
        "longitude": params.lon,
        "daily": [
            "weathercode",
            "temperature_2m_max",
            "temperature_2m_min",
            "sunshine_duration"
        ],
        "hourly": [
            "surface_pressure"
        ],
        "timezone": "auto"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL, params=query)
        # print(f"Request URL: {response.url}")
        # print(f"Status code: {response.status_code}")
        # print(f"Response: {response.text}")

        response.raise_for_status()
        return response.json()



async def get_forecast_data(params: ForecastRequestParams) -> ForecastResponse:
    data = await fetch_weather_data(params)
    daily = data["daily"]
    days = []

    for i in range(len(daily["time"])):
        date_val = date.fromisoformat(daily["time"][i])
        sun_hours = daily["sunshine_duration"][i] / 3600
        energy = round(params.power * sun_hours * params.efficiency, 2)

        day = ForecastDay(
            date=date_val,
            weather_code=daily["weathercode"][i],
            temp_min=daily["temperature_2m_min"][i],
            temp_max=daily["temperature_2m_max"][i],
            energy=energy
        )
        days.append(day)

    return ForecastResponse(forecast=days)


async def get_summary_data(params: ForecastRequestParams) -> SummaryResponse:
    data = await fetch_weather_data(params)
    daily = data["daily"]
    hourly = data["hourly"]

    daily_pressure_map = defaultdict(list)
    for timestamp, pressure in zip(hourly["time"], hourly["surface_pressure"]):
        day = timestamp.split("T")[0]
        daily_pressure_map[day].append(pressure)

    avg_pressures_per_day = [
        sum(pressures) / len(pressures)
        for day, pressures in daily_pressure_map.items()
        if day in daily["time"]
    ]

    avg_pressure = round(sum(avg_pressures_per_day) / len(avg_pressures_per_day), 2)

    sun_durations = daily["sunshine_duration"]
    temp_mins = daily["temperature_2m_min"]
    temp_maxs = daily["temperature_2m_max"]
    weather_codes = daily["weathercode"]

    avg_sun_hours = round(sum(sun_durations) / 3600 / len(sun_durations), 2)
    temp_min = min(temp_mins)
    temp_max = max(temp_maxs)

    rainy_days = sum(1 for code in weather_codes if code >= 50)
    is_rainy_week = rainy_days >= 4


    return SummaryResponse(
        avg_pressure=avg_pressure,
        avg_sun_hours=avg_sun_hours,
        temp_min=temp_min,
        temp_max=temp_max,
        is_rainy_week=is_rainy_week
    )

