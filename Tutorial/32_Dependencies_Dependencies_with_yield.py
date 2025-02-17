from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException

app = FastAPI()
data = {
    "plumbus": {"description": "Freshly", "owner": "Morty"},
    "portal-gun": {"description": "Gun", "owner": "Risk"},
}


# --------------------------------------------------------------------------------------------------------------
# Dependencies with yield and HTTPException
class OwnerError(Exception):
    pass


def get_username():
    try:
        yield "Risk"
    except OwnerError as e:  # Dependencies with yield and except
        raise HTTPException(
            status_code=400, detail=f"OwnerError:{e}"
        )  # Dependencies with yield and HTTPException
        # Always raise in Dependencies with yield and except


@app.get("/items/{item_id}")
def get_item(item_id: str, username: Annotated[str, Depends(get_username)]):
    if item_id not in data:
        raise HTTPException(status_code=404, detail="Item not found")
    item = data[item_id]
    if item["owner"] != username:
        raise OwnerError(username)
    return item
