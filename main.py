from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel 

app = FastAPI()


class Base64Video(BaseModel):
    data: str

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/predict/video")
def predict_from_video(base64Video: Base64Video):
    # Convert to video
    # Extract skeleton
    # Inference model

    return base64Video

