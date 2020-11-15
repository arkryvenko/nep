from app.api.models import UserInDB, UserOut
from app.db import Users, database, fake_hash_password


async def count_by_country():
    query = """select count(users.id) as users_count, users.country as country 
               from users
               group by users.country"""
    return await database.fetch_all(query=query)


async def get_all():
    query = Users.select()
    return await database.fetch_all(query=query)


async def get_by_id(id: int):
    query = Users.select().where(id == Users.c.id)
    return await database.fetch_one(query=query)


async def get_by_username(username: str):
    query = Users.select().where(username == Users.c.username)
    return await database.fetch_one(query=query)


async def delete(id: int):
    query = Users.delete().where(id == Users.c.id)
    return await database.execute(query=query)


async def post(user: UserInDB):
    query = Users \
        .insert() \
        .values(username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                country=user.country,
                password=user.password,
                )
    return await database.execute(query=query)


async def put(id: int, user: UserOut):
    query = Users \
        .update() \
        .where(id == Users.c.id) \
        .values(username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                country=user.country,
                )
    return await database.execute(query=query)
