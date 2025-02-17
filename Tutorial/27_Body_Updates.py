from typing import Optional
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


# --------------------------------------------------------------------------------------------------------------
# Update replacing with PUT
class Item(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items_1/{item_id}", response_model=Item)
async def read_item_1(item_id: str):
    return items[item_id]


@app.put("/items_1/{item_id}", response_model=Item)
async def update_item_1(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded


# --------------------------------------------------------------------------------------------------------------
# Partial updates with PATCH
@app.patch("/items_3/{item_id}", response_model=Item)
async def update_item_2(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.model_dump(
        exclude_unset=True
    )  # Using Pydantic's exclude_unset parameter
    updated_item = stored_item_model.model_copy(
        update=update_data
    )  # Using Pydantic's update parameter
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item
