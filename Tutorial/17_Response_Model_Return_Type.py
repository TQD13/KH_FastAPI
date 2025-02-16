import re
from typing import Annotated, List, Optional, Union
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, EmailStr

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []


@app.post("/items/", response_model=Item)  # Responsible Model Parameter
async def create_item(item: Item) -> Item:
    return item


@app.get("/items/", response_model=List[Item])
async def read_items() -> List[Item]:
    return {
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    }


# --------------------------------------------------------------------------------------------------------------
# Return the same input data
class UserIn_1(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


@app.post("/user/")  # Don't do this in production!
async def create_user_1(user: UserIn_1) -> UserIn_1:
    return user


# --------------------------------------------------------------------------------------------------------------
# Add an output Model
class UserIn_2(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None


class UserOut_2(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


@app.post("/user/", response_model=UserOut_2)
async def create_user_2(user: UserIn_2) -> UserOut_2:
    return user


# --------------------------------------------------------------------------------------------------------------
# Return Type and Data Filtering
class BaseUser_3(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserIn_3(BaseUser_3):
    password: str


@app.post("/user/")
async def create_user_3(user: UserIn_3) -> BaseUser_3:
    return user


# --------------------------------------------------------------------------------------------------------------
# Other Return Type Annotations
# Return a Response Directly
@app.get("/portal_1/")
async def get_portal_1(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="google.com")
    return JSONResponse(content={"message": "Here's your"})


# --------------------------------------------------------------------------------------------------------------
# Annotate a Response Subclass
@app.get("/teleport/")
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.google.com")


# --------------------------------------------------------------------------------------------------------------
# # Invalid Return Type Annotations
# @app.get("/portal_2")
# async def get_portal_2(teleport: bool = False) -> Union[Response, dict]:
#     if teleport:
#         return RedirectResponse(url="https://www.google.com")
#     return {"message": "Here's your"}


# --------------------------------------------------------------------------------------------------------------
# Disable Response Model
@app.get("/portal_3", response_model=None)
async def get_portal_3(teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://www.google.com")
    return {"message": "Here's your"}


# --------------------------------------------------------------------------------------------------------------
# Response Model encoding parameters
class Item_2(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items_2/{item_id}", response_model=Item_2, response_model_exclude_unset=True)
async def read_item_2(item_id: str):
    return items[item_id]
