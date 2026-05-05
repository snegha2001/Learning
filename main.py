from fastapi import FastAPI
from enum import Enum

app = FastAPI()

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


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
        
