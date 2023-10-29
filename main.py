import os
from contextlib import asynccontextmanager
from typing import Union
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from services.utility import base64ToVideo, remove_video_file
from services.skeleton_extraction import extract_skeleton
from services.lstm import LSTM
load_dotenv()
class Base64Video(BaseModel):
    data: str


ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["lstm_model"] = LSTM({'break': 0, 'evening': 1, 'five': 2, 'good': 3, 'stand': 4, 'time': 5}, int(os.getenv("MAX_FRAMES")), int(os.getenv("STEP_SIZE")))
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()


app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/predict/video")
def upload(video: Base64Video):
    # Convert base64 to mp4
    fileName = base64ToVideo(video.data)

    if(not fileName):
        return {"message": "Invalid file"}
    
    # If the video file is not in 720x720, change it
    
    # Extract skeleton
    x, y = extract_skeleton(fileName)
    print(x.shape, y.shape)

    # Predict sign
    predicted_class = ml_models['lstm_model'].predict(x, y)

    remove_video_file(fileName)

    if(not predicted_class):
        return {"message:" "Could not predict sign"}

    
    return {"sign": predicted_class}

        
    

