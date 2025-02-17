from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items_1/")
async def read_items_1(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
