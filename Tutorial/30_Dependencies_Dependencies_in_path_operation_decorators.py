from typing import Annotated
from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()


async def verify_token_1(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X_Token header invalid")


async def verify_key_1(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X_Key header invalid")
    return x_key


@app.get(
    "/items_1/",
    dependencies=[
        Depends(verify_token_1),
        Depends(verify_key_1),
    ],  # Add dependencies to the path operation decorator
)
async def read_items_1():
    return [{"item": "Foo"}, {"item": "Bar"}]


# --------------------------------------------------------------------------------------------------------------
# Dependencies errors and return values
async def verify_token_2(x_token: Annotated[str, Header()]):  # Dependency requirements
    if x_token != "fake-super-secret-token":
        raise HTTPException(
            status_code=400, detail="X_Token header invalid"
        )  # Raise exceptions


async def verify_key_2(x_key: Annotated[str, Header()]):  # Dependency requirements
    if x_key != "fake-super-secret-key":
        raise HTTPException(
            status_code=400, detail="X-Key header invalid"
        )  # Raise exceptions
    return x_key  # Return values


@app.get("/items_2/", dependencies=[Depends(verify_token_2), Depends(verify_key_2)])
async def read_items_2():
    return [{"item": "Foo"}, {"item": "Bar"}]
