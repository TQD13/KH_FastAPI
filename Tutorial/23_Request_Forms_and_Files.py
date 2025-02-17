from typing import Annotated
from fastapi import FastAPI, File, Form, UploadFile  # Import File and Form

app = FastAPI()


@app.post("/files/")
async def create_file(  # Define File and Form Parameters
    file: Annotated[bytes, File()],
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()],
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }
