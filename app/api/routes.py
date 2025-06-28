from fastapi import APIRouter, Query, HTTPException
from app.models.request import ForecastRequestParams
from app.models.response import ForecastResponse, SummaryResponse
from app.services.weather import get_forecast_data, get_summary_data
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/forecast", response_model=ForecastResponse)
async def forecast(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
    power: float = Query(2.5, gt=0, description="Installation power in kW"),
    efficiency: float = Query(0.2, gt=0, le=1, description="Panel efficiency (0 < eff ≤ 1)")
):
    try:
        params = ForecastRequestParams(lat=lat, lon=lon, power=power, efficiency=efficiency)
        return await get_forecast_data(params)
    except Exception as e:
        logger.exception("Error fetching forecast data:")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary", response_model=SummaryResponse)
async def summary(
    lat: float = Query(..., ge=-90, le=90, description="Latitude"),
    lon: float = Query(..., ge=-180, le=180, description="Longitude"),
    power: float = Query(2.5, gt=0, description="Installation power in kW"),
    efficiency: float = Query(0.2, gt=0, le=1, description="Panel efficiency (0 < eff ≤ 1)")
):
    try:
        params = ForecastRequestParams(lat=lat, lon=lon, power=power, efficiency=efficiency)
        return await get_summary_data(params)
    except Exception as e:
        logger.exception("Error fetching forecast data:")
        raise HTTPException(status_code=500, detail=str(e))
