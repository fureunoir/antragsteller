from os import getenv
from typing import List

from fastapi import HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient

from src.handlers import router
from src.helpers.user import (
    add_user,
    retrieve_user,
    update_user,
    delete_user, retrieve_users,
)
from src.models.user import UserModel


# Dependency for getting the MongoDB users collection
async def get_users_collection():
    client = AsyncIOMotorClient(getenv("MONGO_URI", "mongodb://localhost:27017"))
    db = client["antragsteller"]
    return db.get_collection("users")

# Route to get all users
@router.get("/users", response_description="List all users", response_model=List[UserModel] | dict)
async def get_users(admin_key: str, users_collection=Depends(get_users_collection)):
    if admin_key != getenv("ADMIN_KEY"):
        return {"msg": "FUCK OFF"}
    users = await retrieve_users(users_collection)
    return users


# Route to add a user
@router.post("/users", response_description="Add new user", response_model=UserModel | dict)
async def create_user(admin_key: str, user: UserModel, users_collection=Depends(get_users_collection)):
    if admin_key != getenv("ADMIN_KEY"):
        return {"msg": "FUCK OFF"}
    user_exists = await retrieve_user(users_collection, user.telegram_id)
    if user_exists:
        raise HTTPException(status_code=400, detail="User already exists.")
    new_user = await add_user(users_collection, user)
    return new_user

# Route to get a user by telegram_id
@router.get("/users/{telegram_id}", response_description="Get a user by Telegram ID", response_model=UserModel | dict)
async def get_user(admin_key: str, telegram_id: int, users_collection=Depends(get_users_collection)):
    if admin_key != getenv("ADMIN_KEY"):
        return {"msg": "FUCK OFF"}
    user = await retrieve_user(users_collection, telegram_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

# Route to update a user
@router.put("/users/{telegram_id}", response_description="Update a user", response_model=UserModel | dict)
async def update_user_data(admin_key: str, telegram_id: int, data: UserModel, users_collection=Depends(get_users_collection)):
    if admin_key != getenv("ADMIN_KEY"):
        return {"msg": "FUCK OFF"}
    updated = await update_user(users_collection, telegram_id, data.model_dump(exclude_unset=True))
    if updated:
        return await retrieve_user(users_collection, telegram_id)
    raise HTTPException(status_code=404, detail="User not found")

# Route to delete a user
@router.delete("/users/{telegram_id}", response_description="Delete a user")
async def delete_user_data(admin_key: str, telegram_id: int, users_collection=Depends(get_users_collection)):
    if admin_key != getenv("ADMIN_KEY"):
        return {"msg": "FUCK_OFF"}
    deleted = await delete_user(users_collection, telegram_id)
    if deleted:
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")
