from typing import Union
from typing import List
from fastapi import FastAPI
from dotenv import load_dotenv

from app.utils.async_utils import lifespan
from app.routers.predict import router

load_dotenv()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


app.include_router(router, prefix="/predict")


        
    
