from app.api.models import UserCreate, UserOut
from app.db import Users, database


async def get_all():
    query = Users.select()
    return await database.fetch_all(query=query)


async def get(id: int):
    query = Users.select().where(id == Users.c.id)
    return await database.fetch_one(query=query)


async def delete(id: int):
    query = Users.delete().where(id == Users.c.id)
    return await database.execute(query=query)


async def post(user: UserCreate):
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
