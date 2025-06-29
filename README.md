# Weather Forecast API (Backend)

## Project Overview

This is a **backend application** built with **FastAPI** for:

- Fetching 7-day weather forecasts using the [Open-Meteo API](https://open-meteo.com/)
- Estimating solar energy production
- Providing a summarized weekly weather report

The backend is containerized and ready to deploy using Docker.

> **Note**: This repository includes only the backend. The frontend is developed and documented separately.

---

## Tech Stack

- Python 3.10+
- FastAPI
- httpx (async HTTP client)
- Pydantic (data validation)
- Pytest (unit testing)
- Docker

---

## Running the App

### Requirements

- [Docker](https://www.docker.com/) (recommended)
- Alternatively: Python 3.10+ with `pip` (instruction not specified)

---

### Run with Docker (recommended)

```bash
# Build the Docker image
docker build -t weather-backend .

# Run the container
docker run -p 8000:8000 weather-backend
```

Access the API at:  
**http://localhost:8000**

Interactive Swagger UI:  
**http://localhost:8000/docs**

---

## API Endpoints

### `GET /forecast`

Returns a 7-day weather forecast and estimated solar energy output.

**Query Parameters**:
- `lat` – latitude (required)
- `lon` – longitude (required)
- `power` – solar panel power in kW (default: `2.5`)
- `efficiency` – panel efficiency [0–1] (default: `0.2`)

**Example**:
```
/forecast?lat=50.06&lon=19.94&power=3.0&efficiency=0.18
```

**Sample Response**:
```json
{
  "forecast": [
    {
      "date": "2025-06-29",
      "weather_code": 2,
      "temp_min": 16.5,
      "temp_max": 25.1,
      "energy": 4.32
    }
  ]
}
```

---

### `GET /summary`

Returns weekly weather statistics and a general atmospheric summary.

**Sample Response**:
```json
{
  "avg_pressure": 1012.4,
  "avg_sun_hours": 6.5,
  "temp_min": 14.2,
  "temp_max": 27.9,
  "is_cloudy_week": true
}
```

---

## Testing

To run unit tests:

```bash
docker run --rm -v $PWD:/app -w /app weather-backend pytest tests/
```

Test coverage includes:
- Data models
- Forecast & summary logic
- API routes

---

## Environment Variables

Define settings in a `.env` file:

```
ALLOWED_ORIGINS
```

The `.env` file is automatically loaded using `python-dotenv`.

---

## Deployment

This backend is ready for deployment on any container-based platform such as:

- Render
- Railway
- Fly.io
- Your own VPS

The included `Dockerfile` handles everything.

