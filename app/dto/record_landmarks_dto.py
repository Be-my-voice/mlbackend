from pydantic import BaseModel, validator
from typing import List

from pyparsing import Any

class JsonLandmarkRes(BaseModel):
    landmarks: List[List[Any]]
    message: str

    def setLandmarks(self, landmarks: List[List[Any]]):
        self.landmarks.append(landmarks)

    def setMessage(self, message: str):
        self.message = message
