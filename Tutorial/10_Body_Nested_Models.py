from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from typing import List, Union

app = FastAPI()


# --------------------------------------------------------------------------------------------------------------
# Lsit fields
class Item_1(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list = []


@app.put("/items_1/{item_id}")
async def update_item_1(item_id: int, item: Item_1):
    results = {"item_id": item_id, "item": item}
    return results


# --------------------------------------------------------------------------------------------------------------
# List fields with type parameter
class Item_2(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags_1: list[str] = []  # Delare a lsit with a type parameter
    tags_2: set[str] = set()  # Set types


@app.put("/items_2/{item_id}")
async def update_item_2(item_id: int, item: Item_2):
    results = {"item_id": item_id, "item": item}
    return results


# --------------------------------------------------------------------------------------------------------------
# Nested Models
class Image_3(BaseModel):
    url: str
    name: str
    url_spec: str  # Special types and validation


class Item_3(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image_3 | None = None  # Use submodel as a type
    image_atr: list[Image_3] | None = None  # Attributes with lsits of submodel


@app.put("/items_3/{item_id}")
async def update_item_3(item_id: int, item: Item_3):
    results = {"item_id": item_id, "item": item}
    return results


# --------------------------------------------------------------------------------------------------------------
# Bodies of pure lists


class Image_4(BaseModel):
    url: HttpUrl
    name: str


@app.post("/images_4/multiple/")
async def create_multiple_images(images: list[Image_4]):
    return images


# --------------------------------------------------------------------------------------------------------------
# Bodies of arbitrary dicts
@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights
