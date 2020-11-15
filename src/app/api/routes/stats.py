from http import HTTPStatus
from fastapi import APIRouter
from app.api import crud

router = APIRouter()


@router.get("/", status_code=HTTPStatus.OK)
async def retrieve_stats():
    all = await crud.count_all()
    by_country = await crud.count_by_country()
    return by_country
