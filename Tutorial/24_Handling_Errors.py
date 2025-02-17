from fastapi import FastAPI, Request, status, HTTPException  # Import HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()
items = {"foo": "The Foo Wrestlers"}


@app.get("/items_1/{items}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404, detail="Item not found"
        )  # Raise an HTTPException in your code
    return {"item": items[item_id]}


# -----------------------------------------------------------------------------------------
# Add custom headers
@app.get("/items-header_1/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}


# -----------------------------------------------------------------------------------------
# Install custom exception handlers
class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops {exc.name} did something. There goes a rainbow"},
    )


@app.get("/unicorns_1/{name}")
async def read_unicorn_1(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


# -----------------------------------------------------------------------------------------
# Override the default exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler_2(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/items_2/{item_id}")
async def read_item_2(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}


# -----------------------------------------------------------------------------------------
# Override the HTTPException error handler
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler_3(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler_3(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/items_3/{item_id}")
async def read_item_3(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}


# -----------------------------------------------------------------------------------------
# Use the RequestValidationError body
@app.exception_handler(RequestValidationError)
async def validation_exception_handler_4(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


class Item_4(BaseModel):
    title: str
    size: int


@app.post("/items/")
async def create_item_4(item: Item_4):
    return item


# -----------------------------------------------------------------------------------------
# Reuse FastAPI's exception handlers
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler_5(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler_5(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)


@app.get("/items_5/{item_id}")
async def read_item_5(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}
