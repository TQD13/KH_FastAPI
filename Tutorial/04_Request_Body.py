from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):  # Create data model
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items/")
async def create_item(item: Item):  # Declare data model as a parameter
    return item


# --------------------------------------------------------------------------------------------------------------
# Use the model
@app.post("/items/")
async def create_item_1(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# --------------------------------------------------------------------------------------------------------------
# Request Body and Path parameters
@app.put("/items/{item_id}")
async def update(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}


# --------------------------------------------------------------------------------------------------------------
# Request Body + Path + Query parameters
@app.put(("/items/{item_id}"))
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result

