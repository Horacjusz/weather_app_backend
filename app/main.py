from fastapi import FastAPI
from app.api.routes import router
import uvicorn

app = FastAPI(
    title="Weather Forecast API",
    description="Provides 7-day weather forecasts and solar energy estimates based on location.",
    version="1.0.0"
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
