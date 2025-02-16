from typing import Annotated, List, Optional
from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()


class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: Optional[str] = None
    traceparent: Optional[str] = None
    x_tag: List[str] = []


@app.get("/items/")
async def read_items(
    host: Annotated[str, Header()],
    save_data: Annotated[bool, Header()],
    if_modified_since: Annotated[Optional[str], Header()] = None,
    traceparent: Annotated[Optional[str], Header()] = None,
    x_tag: Annotated[List[str], Header()] = [],
):
    headers = CommonHeaders(
        host=host,
        save_data=save_data,
        if_modified_since=if_modified_since,
        traceparent=traceparent,
        x_tag=x_tag,
    )
    return headers


# --------------------------------------------------------------------------------------------------------------
# Forbid Extra Headers sample as Query Parameter Models
