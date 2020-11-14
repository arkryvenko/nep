from typing import List

from app.api import crud
from app.api.models import UserCreate, UserOut, UserBase
from fastapi import APIRouter, HTTPException, Path

router = APIRouter()


async def _get_or_404(id: int):
    user = await crud.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=List[UserOut])
async def retrieve_all_users():
    return await crud.get_all()


@router.get("/{id}/", response_model=UserOut)
async def retrieve_single_user(id: int = Path(..., gt=0)):
    return await _get_or_404(id)


@router.post("/", response_model=UserOut, status_code=201)
async def create_user(user: UserCreate):
    last_record_id = await crud.post(user)
    response = {**user.dict(), "id": last_record_id}
    return response


@router.put("/{id}/", response_model=UserOut)
async def update_user(updated_user: UserBase, id: int = Path(..., gt=0)):
    user = await _get_or_404(id)
    await crud.put(id, updated_user)
    response = {**updated_user.dict(), "id": user.id}
    return response


@router.delete("/{id}/", status_code=204)
async def delete_user(id: int = Path(..., gt=0)):
    user = await _get_or_404(id)
    await crud.delete(user.id)
    return None
