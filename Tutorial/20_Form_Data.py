from typing import Annotated
from fastapi import FastAPI, Form  # Import Form

app = FastAPI()


@app.post("/login/")
async def login(
    username: Annotated[str, Form()], password: Annotated[str, Form()]
):  # Define Form Parameters
    return {"username": username}
