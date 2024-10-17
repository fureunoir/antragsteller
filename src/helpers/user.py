from motor.motor_asyncio import AsyncIOMotorCollection
from src.models.user import UserModel
from typing import List

# Helper function to format MongoDB user data
def user_helper(user) -> dict:
    return {
        "telegram_id": user["telegram_id"],
        "first_name": user.get("first_name"),
        "last_name": user.get("last_name"),
        "is_admin": user.get("is_admin", False),
        "is_active": user.get("is_active", True),
    }

# Add user to the database
async def add_user(users_collection: AsyncIOMotorCollection, user_data: UserModel) -> dict:
    user = await users_collection.insert_one(user_data.model_dump())
    new_user = await users_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

# Retrieve all users
async def retrieve_users(users_collection: AsyncIOMotorCollection) -> List[dict]:
    users = []
    async for user in users_collection.find():
        users.append(user_helper(user))
    return users

# Retrieve a user by telegram_id
async def retrieve_user(users_collection: AsyncIOMotorCollection, telegram_id: int) -> dict:
    user = await users_collection.find_one({"telegram_id": telegram_id})
    if user:
        return user_helper(user)
    return {}

# Update a user
async def update_user(users_collection: AsyncIOMotorCollection, telegram_id: int, data: dict) -> bool:
    if len(data) < 1:
        return False
    user = await users_collection.find_one({"telegram_id": telegram_id})
    if user:
        updated_user = await users_collection.update_one(
            {"telegram_id": telegram_id}, {"$set": data}
        )
        if updated_user.modified_count > 0:
            return True
    return False

# Delete a user
async def delete_user(users_collection: AsyncIOMotorCollection, telegram_id: int) -> bool:
    user = await users_collection.find_one({"telegram_id": telegram_id})
    if user:
        await users_collection.delete_one({"telegram_id": telegram_id})
        return True
    return False
