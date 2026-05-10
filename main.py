from fastapi import Depends, FastAPI, HTTPException, Query, Path, Form
from enum import Enum
from pydantic import BaseModel
from typing import Annotated
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


app = FastAPI()



class FormData(BaseModel):
    username: str
    password: str

student = {
    1: {"name": "Rick", "age": 70},
    2: {"name": "Morty", "age": 14}
}

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
async def read_item(id: int):
    return {"message": id}

@app.get("/students/{id}")
async def read_student(id: int = Path(..., title="The ID of the student to get", ge=1, le=2)):
    return student[id]

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

@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

    
@app.post("/heroes/")
def create_hero(hero: Hero, session: SessionDep) -> Hero:
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@app.get("/heroes/")
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Hero]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.get("/heroes/{hero_id}")
def read_hero(hero_id: int, session: SessionDep) -> Hero:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
        
