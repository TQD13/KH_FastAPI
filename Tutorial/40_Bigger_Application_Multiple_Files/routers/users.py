# API Router
from fastapi import APIRouter  # Import APIRouter

router = APIRouter()


@router.get("/users/", tags=["users"])  # Path operations with APIRouter
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])  # Path operations with APIRouter
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])  # Path operations with APIRouter
async def read_user(username: str):
    return {"username": username}
