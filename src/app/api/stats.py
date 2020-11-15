from fastapi import APIRouter, Depends
from app.api import crud

router = APIRouter()


@router.get("/")
async def retrieve_stats():
    return {'hello': 'world'}
