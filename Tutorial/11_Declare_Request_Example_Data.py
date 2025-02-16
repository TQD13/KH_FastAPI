from fastapi import Body, FastAPI
from pydantic import BaseModel, Field
from typing import Annotated

app = FastAPI()
# --------------------------------------------------------------------------------------------------------------
# Extra JSON Schema data in Pydantic models


class Item_1(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }


@app.put("/items_1/{item_id}")
async def update_item_1(item_id: int, item: Item_1):
    results = {"item_id": item_id, "item": item}
    return results


# --------------------------------------------------------------------------------------------------------------
# Field additional arguments
class Item_2(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35.4])
    tax: float | None = Field(default=None, examples=[3, 2])


@app.put("/items_2/{item_id}")
async def update_item_2(item_id: int, item: Item_2):
    results = {"item_id": item_id, "item": item}
    return results


# --------------------------------------------------------------------------------------------------------------
# examples in JSON Schema - OpenAPI
class Item_3(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items_3/{item_id}")
async def update_item_3(
    *,
    item_id: int,
    item: Annotated[
        Item_3,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal item works correctly",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "Third five point four",
                    },
                },
            },
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results
