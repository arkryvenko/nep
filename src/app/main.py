import uvicorn
from fastapi import FastAPI

from logger import init_logger
from db import database, engine, metadata
from api.routes import stats, users, auth


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()
    await init_logger()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(stats.router, tags=["statistics"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True, debug=True, workers=1)
