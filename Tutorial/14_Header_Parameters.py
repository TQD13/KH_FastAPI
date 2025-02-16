from fastapi import FastAPI, Header
from typing import Annotated

app = FastAPI()


@app.get("/items_1/")
async def read_items_1(
    user_agent: Annotated[str | None, Header()] = None,
):  # Declare Header Parameters
    return {"user_agent": user_agent}


@app.get("/items_2/")
async def read_items_2(
    strange_header: Annotated[
        str | None, Header(convert_underscores=False)
    ] = None,  # Automatic Convertion
):
    return {"strange_header": strange_header}


@app.get("/items/")
async def read_items_3(
    x_token: Annotated[list[str] | None, Header()] = None,
):  # Duplicate Headers
    return {"X-Token values": x_token}
