from typing import List
from loguru import logger
from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Path, Depends
from fastapi.responses import JSONResponse

from api import crud
from api.routes import auth
from api.models import UserInDB, UserOut, UserBase

router = APIRouter()


async def get_by_id_or_404(id: int):
    user = await crud.get_by_id(id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user


@router.get("/", response_model=List[UserOut], status_code=HTTPStatus.OK)
async def retrieve_all_users(token: str = Depends(auth.oauth2_scheme)):
    return await crud.get_all()


@router.get("/{id}/", response_model=UserOut, status_code=HTTPStatus.OK)
async def retrieve_user(id: int = Path(..., gt=0), token: str = Depends(auth.oauth2_scheme)):
    return await get_by_id_or_404(id)


@router.post("/", response_model=UserOut, status_code=HTTPStatus.CREATED)
async def create_user(user: UserInDB, token: str = Depends(auth.oauth2_scheme)):
    user_db = await crud.get_by_username(user.username)
    if user_db:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=f"The username '{user.username}' already exists. Please use a different username.",
        )
    user.password = auth.get_password_hash(user.password)
    last_record_id = await crud.create_user(user)
    response = {**user.dict(), "id": last_record_id}
    logger.info(f"User ID: {last_record_id} created")
    return response


@router.put("/{id}/", response_model=UserOut, status_code=HTTPStatus.OK)
async def update_user(updated_user: UserBase, id: int = Path(..., gt=0), token: str = Depends(auth.oauth2_scheme)):
    user = await get_by_id_or_404(id)
    await crud.update_user(id, updated_user)
    response = {**updated_user.dict(), "id": user.id}
    logger.info(f"User ID: {id} updated")
    return response


@router.delete("/{id}/")
async def delete_user(id: int = Path(..., gt=0), token: str = Depends(auth.oauth2_scheme)):
    user = await get_by_id_or_404(id)
    await crud.delete_user(user.id)
    logger.info(f"User ID: {id} deleted")
    return JSONResponse(status_code=HTTPStatus.OK, content={"message": "User has been deleted"})
