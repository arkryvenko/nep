from http import HTTPStatus
from fastapi import APIRouter
from app.api import crud

router = APIRouter()


@router.get("/", status_code=HTTPStatus.OK)
async def retrieve_stats():
    total_users = await crud.count_all()
    users_per_country = await crud.count_per_country()
    stats = {'Total users count': total_users[0], 'Users per country': users_per_country}
    return stats
