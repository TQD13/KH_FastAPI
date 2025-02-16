from fastapi import FastAPI, Query
from typing import Annotated

app = FastAPI()


@app.get("/items_1/")
async def read_items_1(q: str | None = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# --------------------------------------------------------------------------------------------------------------
# Additional Validation


@app.get("/items_2/")
async def read_items_2(
    q: Annotated[  # Add
        str | None, Query(max_length=50)
    ] = None,
):  # Add Query to Annotated (min_length, max_length, pattern or regex,...(ellipsis), None) in the q parameter
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
