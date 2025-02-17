from fastapi import FastAPI, status

app = FastAPI()


@app.post("/items_1/", status_code=201)
async def create_item_1(name: str):
    return {"name": name}


# -----------------------------------------------------------------------------------------
# Shortcut to remember the names
@app.post("/items_2/", status_code=status.HTTP_201_CREATED)
async def create_item_2(name: str):
    return {"name": name}
