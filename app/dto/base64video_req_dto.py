from pydantic import BaseModel

class Base64Video(BaseModel):
    data: str
