from contextlib import asynccontextmanager
from typing import Union
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from src.utility import base64ToVideo
from src.skeleton_extraction import extract_skeleton
from src.lstm import LSTM

class Base64Video(BaseModel):
    data: str


ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["lstm_model"] = LSTM({'break': 0, 'evening': 1, 'five': 2, 'good': 3, 'stand': 4, 'time': 5}, 120, 3)
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
        return {"message:" "We fucked up"}
    
    # Extract skeleton
    x, y = extract_skeleton(fileName)
    print(x.shape, y.shape)

    # Predict sign
    predicted_class = ml_models['lstm_model'].predict(x, y)

    if(not predicted_class):
        return {"message:" "Could not predict sign"}

    # return {'x': x, 'y': y}
    return {"sign": predicted_class}

        
    

