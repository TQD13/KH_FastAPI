from re import purge
from typing import Annotated
from fastapi import Body, FastAPI, Path
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


# --------------------------------------------------------------------------------------------------------------
# Mix Path, Query and body parameters
@app.put("/items_1/{item_id}")
async def update_item_1(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


# --------------------------------------------------------------------------------------------------------------
# Multiple body parameters
@app.put("/items_2/{item_id}")
async def update_item_2(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results


# --------------------------------------------------------------------------------------------------------------
# Singular values in body
@app.put("/items_3/{item_id}")
async def update_item_3(
    item_id: int, item: Item, user: User, importance: Annotated[int, Body()]
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


# --------------------------------------------------------------------------------------------------------------
# Multiple body params and query
@app.put("/items_4/{item_id}")
async def update_item_4(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body(gt=0)],
    q: str | None = None,
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results


# --------------------------------------------------------------------------------------------------------------
# Embed a single body parameter
@app.put("/items_5/{item_id}")
async def update_item_5(item_id: int, item=Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results
