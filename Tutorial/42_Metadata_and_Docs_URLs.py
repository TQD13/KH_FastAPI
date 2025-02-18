from fastapi import FastAPI

# Create metadata for tags
description = """  
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

app = FastAPI(
    title="ChimichangApp",
    description=description,
    summary="Deadpool's favorite app. Nuff said.",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


@app.get("/items/")
async def read_items():
    return [{"name": "Katana"}]


# --------------------------------------------------------------------------------------------------------------
# OpenAPI URL
app_2 = FastAPI(openapi_url="/apo/v1/openapi.json")  #


@app_2.get("/items_2/")
async def read_items_2():
    return [{"name": "Foo"}]


# --------------------------------------------------------------------------------------------------------------
# Docs URLs
app_3 = FastAPI(docs_url="/documentation", redoc_url=None)


@app_3.get("/items_3/")
async def read_items_3():
    return [{"name": "Foo"}]
