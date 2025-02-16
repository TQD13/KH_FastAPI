from typing import List, Optional, Union
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: Optional[str] = None


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_password_hasher(user_in)
    return user_saved


# --------------------------------------------------------------------------------------------------------------
# Reduce application
class UserBase_2(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserIn_2(UserBase_2):
    password: str


class UserOut_2(UserBase_2):
    pass


class UserInDB_2(UserBase_2):
    hashed_password: str


def fake_password_hasher_2(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user_2(user_in: UserIn_2):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB_2(**user_in.model_dump(), hashed_password=hashed_password)
    print("User saved! not really")
    return user_in_db


@app.post("/users_2/", response_model=UserOut_2)
async def create_user_2(user_in: UserIn_2):
    user_saved = fake_save_user(user_in)
    return user_saved


# --------------------------------------------------------------------------------------------------------------
# Union or anyOf
class BaseItem_3(BaseModel):
    description: str
    type: str


class CarItem_3(BaseItem_3):
    type: str = "car"


class PlaneItem_3(BaseItem_3):
    type: str = "plane"
    size: int


items_3 = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


@app.get("/items_3/{item_id}", response_model=Union[PlaneItem_3, CarItem_3])
async def read_item_3(item_id: str):
    return items_3[item_id]


# --------------------------------------------------------------------------------------------------------------
# List of models
class Item_4(BaseModel):
    name: str
    description: str


items_4 = [
    {"name": "Foo", "description": "Here's your"},
    {"name": "Red", "description": "It's my"},
]


@app.get("/items_4/", response_model=list[Item_4])
async def read_item_4():
    return items_4


# --------------------------------------------------------------------------------------------------------------
# Response with arbitrary dict
@app.get("/keyword-weights/", response_model=dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}
