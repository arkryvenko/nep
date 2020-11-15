import os

from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table, create_engine)
from sqlalchemy.sql import func

from databases import Database

# sqlite
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
metadata = MetaData()

Users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(32), unique=True, nullable=False),
    Column("first_name", String(50)),
    Column("last_name", String(50)),
    Column("email", String(50)),
    Column("country", String(50)),
    Column("password", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)


def fake_hash_password(password: str):
    return f"fakehashed{password}"


# databases query builder
database = Database(DATABASE_URL)
