from fastapi import FastAPI
from enum import Enum

app = FastAPI()


@app.get("/item/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


# --------------------------------------------------------------------------------------------------------------
# Oder Matters
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


# --------------------------------------------------------------------------------------------------------------
# Predefinded values
class ModelName(str, Enum):  # Enum class
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):  # Declare a path parameter
    if model_name is ModelName.alexnet:  # Compare enumeration memebers
        return {"model_name": model_name, "message": "Deep Leanring FTW"}
    if model_name.value == "lenet":  # Get the enumeration value
        return {"model_name": model_name, "message": "LeCNN all the  imagages"}
    return {
        "model_name": model_name,
        "message": "Have some residuals",
    }  # Return enumeration members


# --------------------------------------------------------------------------------------------------------------
# Path parameters containing paths
@app.get("/files/{file_path:path}")  # Path convertor
async def read_file(file_path: str):
    return {"file_path": file_path}

