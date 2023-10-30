from pydantic import BaseModel, validator
from typing import List

class JsonLandmark(BaseModel):
    landmarks: List[List[float]]

    @validator('landmarks')
    def check_sublist_length(cls, value):
        for sublist in value:
            if len(sublist) != 24:
                raise ValueError("Each sublist must have a length of 24")
        return value
