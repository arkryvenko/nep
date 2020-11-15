from fastapi import APIRouter
from app.api import crud

router = APIRouter()


@router.get("/")
async def retrieve_stats():
    return await crud.count_by_country()

