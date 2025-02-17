from typing import Annotated, Optional
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel  # Create a user model

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="join@example.com", full_name="John Doe"
    )


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
):  # Create a get_current_user dependency
    user = fake_decode_token(token)  # Get the user
    return user


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):  # Inject the current user
    return current_user
