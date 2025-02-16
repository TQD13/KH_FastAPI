from typing import Annotated, Optional
from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Cookies(BaseModel):
    session_id: str
    fatebook_tracker: Optional[str] = None
    googall_tracker: Optional[str] = None


@app.get("/items/")
async def read_items(
    session_id: Annotated[str, Cookie()],
    fatebook_tracker: Annotated[Optional[str], Cookie()] = None,
    googall_tracker: Annotated[Optional[str], Cookie()] = None,
):
    cookies = Cookies(
        session_id=session_id,
        fatebook_tracker=fatebook_tracker,
        googall_tracker=googall_tracker,
    )
    return cookies


# --------------------------------------------------------------------------------------------------------------
# Forbid Extra Cookies, sampple as Quey Parameter Models
