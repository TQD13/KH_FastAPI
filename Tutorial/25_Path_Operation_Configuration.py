from fastapi import FastAPI, status
from pydantic import BaseModel
from enum import Enum

app = FastAPI()


# -----------------------------------------------------------------------------------------
# Response Status Code
class Item_1(BaseModel):
    name: str
    description: str
    price: float
    tax: float | None = None
    tags: set[str] = set()


@app.post("/items_1/", response_model=Item_1, status_code=status.HTTP_201_CREATED)
async def create_item_1(item: Item_1):
    return item


# -----------------------------------------------------------------------------------------
# Tags
@app.post("/items_2/", response_model=Item_1, tags=["items"])
async def create_item_2(item: Item_1):
    return item


@app.get("/items_2/", tags=["items"])
async def read_items_2():
    return [{"name": "Foo", "price": 42}]


@app.get("/users/", tags=["users"])
async def read_users_2():
    return [{"username": "johndoe"}]


# -----------------------------------------------------------------------------------------
# Tags with Enums
class Tags_3(Enum):
    items = "items"
    users = "users"


@app.get("/items_3/", tags=[Tags_3.items])
async def get_items_3():
    return ["Portal gun", "Plumbus"]


@app.get("/users_3/", tags=[Tags_3.users])
async def read_users_3():
    return ["Risk", "Morty"]


# -----------------------------------------------------------------------------------------
# Summary and description
@app.post(
    "/items_4/",
    response_model=Item_1,
    summary="Create an item 4",
    description="Information",
)
async def create_item_4(item: Item_1):
    return item


# -----------------------------------------------------------------------------------------
# Description from docstring
@app.post(
    "/items_5/",
    response_model=Item_1,
    summary="Create an item 5",
    response_description="The created item 5",  # Can specify response description
)
async def create_item_5(item: Item_1):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item


# -----------------------------------------------------------------------------------------
# Deprecate a path operation


@app.get("/items_6/", tags=["items"])
async def create_item_6():
    return [{"name": "Foo", "price": 42}]


@app.get("/users_6/", tags=["users"])
async def read_users_6():
    return [{"username": "johndoe"}]


@app.get("/elements_6/", tags=["items"], deprecated=True)
async def read_elements_6():
    return [{"item_id": "Foo"}]
