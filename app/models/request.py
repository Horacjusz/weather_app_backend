from pydantic import BaseModel, Field


class ForecastRequestParams(BaseModel):
    lat: float = Field(..., ge=-90, le=90, description="Latitude")
    lon: float = Field(..., ge=-180, le=180, description="Longitude")
    power: float = Field(2.5, gt=0, description="Installation power in kW")
    efficiency: float = Field(0.2, gt=0, le=1, description="Panel efficiency (0 < eff ≤ 1)")
