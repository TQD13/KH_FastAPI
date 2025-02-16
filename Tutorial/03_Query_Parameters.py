from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Barz"}]


# --------------------------------------------------------------------------------------------------------------
# Defaults
@app.get("/items/")
async def read_item_1(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


# --------------------------------------------------------------------------------------------------------------
# Optional parameters
@app.get("/items/{item_id}")
async def read_item_2(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


# --------------------------------------------------------------------------------------------------------------
# Query parameter type conversion
@app.get("/items/{item_id}")
async def read_item_3(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# --------------------------------------------------------------------------------------------------------------
# Multiple path and query parameters
@app.get("/users/{user_id}/items/{item_id}")
async def rea_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# --------------------------------------------------------------------------------------------------------------
# Required query parameters
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item
