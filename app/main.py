from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from dotenv import load_dotenv
import os

load_dotenv()

allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

def create_app() -> FastAPI:
    app = FastAPI(
        title="Weather Forecast API",
        description="Provides 7-day weather forecasts and solar energy estimates based on location.",
        version="1.0.0"
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    return app

app = create_app()
