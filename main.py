from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel

app = FastAPI()

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{id}")
async def root(id: int):
    return {"message": id}

@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]

@app.get("/enum_check/{wrd}")
async def enum_reader(wrd : ModelName):
    if wrd == ModelName.alexnet:
        return "correct"
    else:
        return "wrong"
    
@app.get("/query_check/")
async def query_check(alpha:str, numeric : int):
    return {"result": alpha + "-" + str(numeric)} 

@app.post("/body_check")
async def body_check(item: Item):
    return item
        
