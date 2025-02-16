from fastapi import Depends, FastAPI, Query, Request
from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI()


class FilterParams(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )  # Solution 1: Alternative Approach Forbid Extra
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "upddate_at"] = "created_at"
    tags: list[str] = Field(default_factory=list)


def get_filter_params(
    limit: int = Query(100, gt=0, le=100),
    offset: int = Query(0, ge=0),
    order_by: Literal["created_at", "upddate_at"] = "created_at",
    tags: list[str] = Query([]),
) -> FilterParams:
    return FilterParams(limit=limit, offset=offset, order_by=order_by, tags=tags)


# --------------------------------------------------------------------------------------------------------------
# Solution 2: Forbid Extra Query Parameters
@app.get("/items/")
async def read_items(
    filter_query: Annotated[FilterParams, Depends(get_filter_params)],
):
    return filter_query


class FilterParams_1(BaseModel):
    model_config = {"extra": "forbid"}
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "upddate_at"] = "created_at"
    tags: list[str] = Field(default_factory=list)


def get_filter_params_1(
    request: Request,  # Get row query parameters
    limit: int = Query(100, gt=0, le=100),
    offset: int = Query(0, ge=0),
    order_by: Literal["created_at", "upddate_at"] = "created_at",
    tags: list[str] = Query([]),
) -> FilterParams_1:
    query_params = request.query_params._dict  # Get all query parameters

    allowed_params = {
        "limit",
        "offset",
        "order_by",
        "tags",
    }  # Define allowed query parameters
    extra_params = set(query_params) - allowed_params
    if extra_params:
        raise ValueError(f"Unknown query parameters: {','.join(extra_params)}")
    return FilterParams_1(limit=limit, offset=offset, order_by=order_by, tags=tags)
