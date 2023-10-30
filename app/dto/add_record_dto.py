from pydantic import BaseModel, validator
from typing import List

class AddRecord(BaseModel):
    landmarks: List[List[float]]
    class_name: str

    @validator('landmarks')
    def check_sublist_length(cls, value):
        for sublist in value:
            if len(sublist) != 24:
                raise ValueError("Each sublist must have a length of 24")
        return value
    
    @validator('class_name')
    def check_sublist_length(cls, value):
        if len(value) == 0:
            raise ValueError("Class name is not valid")
        return value
