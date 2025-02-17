from typing import Annotated
from fastapi import FastAPI, File, UploadFile  # Import File
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/files_1/")
async def create_file_1(file: Annotated[bytes, File()]):  # Define File Parameters
    return {"file_size": len(file)}


@app.post("/uploadfile_1/")
async def create_upload_file_1(file: UploadFile):  # File Parameters with UploadFile
    return {"file": file.filename}


# -----------------------------------------------------------------------------------------
# Optional File Upload
@app.post("/files_2/")
async def create_file_2(file: Annotated[bytes, File()] = None):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}


@app.post("/uploadfile_2/")
async def create_upload_file_2(file: Annotated[bytes, File()]):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}


# -----------------------------------------------------------------------------------------
# UploadFile with Additional Metadata
@app.post("/files_3/")
async def create_file_3(
    file: Annotated[bytes, File(description="A file read as bytes")],
):
    return {"file_size": len(file)}


@app.post("/uploadfile_3/")
async def create_upload_file_3(
    file: Annotated[UploadFile, File(description="A file read as UploadFile")],
):
    return {"filename": file.filename}


# -----------------------------------------------------------------------------------------
# Multiple File Uploads
@app.post("/files_4/")
async def create_file_4(files: Annotated[list[bytes], File()]):
    return {"filename": [len(file) for file in files]}


@app.post("/uploadfile_4/")
async def create_upload_file_4(files: list[UploadFile]):
    return {"filename": [file.filename for file in files]}


@app.get("/4")
async def main_4():
    content = """
    <body>
    <form action="/files/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    </body>
    """
    return HTMLResponse(content=content)


# -----------------------------------------------------------------------------------------
# Multiple File Uploads with Additional Metadata
@app.post("/files_5/")
async def create_files_5(
    files: Annotated[list[bytes], File(description="Multiple files as bytes")],
):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles_5/")
async def create_upload_files(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    return {"filenames": [file.filename for file in files]}


@app.get("/5")
async def main_5():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
