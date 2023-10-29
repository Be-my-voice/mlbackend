import os
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.services.lstm import LSTM

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["lstm_model"] = LSTM({'break': 0, 'evening': 1, 'five': 2, 'good': 3, 'stand': 4, 'time': 5}, int(os.getenv("MAX_FRAMES")), int(os.getenv("STEP_SIZE")))
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()


def get_resource(resource):
    return ml_models[resource]