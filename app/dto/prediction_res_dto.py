from pydantic import BaseModel

class Prediction(BaseModel):
    prediction: str
    message: str

