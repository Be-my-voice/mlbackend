from typing import Union
from typing import List
from fastapi import FastAPI, Form, UploadFile, File
from pydantic import BaseModel
import ffmpeg
from io import BytesIO
import base64

from src.utility import base64ToVideo
from src.skeleton_extraction import extract_skeleton

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
def upload(video: Base64Video):
    # Convert base64 to mp4
    fileName = base64ToVideo(video.data)

    if(not fileName):
        return {"message:" "We fucked up"}
    
    # Extract skeleton
    x, y = extract_skeleton(fileName)
    print(x.shape, y.shape)

    # return {'x': x, 'y': y}
    return {"message": "Hello"}

        
    

