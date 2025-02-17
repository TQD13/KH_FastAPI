from typing import Annotated, Optional
from fastapi import Cookie, Depends, FastAPI

app = FastAPI()


def query_extractor(q: Optional[str] = None):  # First dependency "dependable"
    return q


def query_or_cookie_extractor(
    q: Annotated[
        str, Depends(query_extractor)  # Second dependency, "dependable" and "dependant"
    ],
    last_query: Annotated[Optional[str], Cookie()] = None,
):
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(
    query_or_default: Annotated[
        str, Depends(query_or_cookie_extractor)  # Use the dependency
    ],
):
    return {"query_or_cookie": query_or_default}


# --------------------------------------------------------------------------------------------------------------
# Using the same dependency multiple times
# @app.get("/items_2/")
# async def needy_dependency(
#     fresh_value: Annotated[str, Depends(get_value, use_cache=False)],
# ):
#     return {"fresh_value": fresh_value}
