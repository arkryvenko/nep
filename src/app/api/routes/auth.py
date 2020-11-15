from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.db import fake_hash_password
from app.api.models import UserInDB
from app.api.crud import get_by_username

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = await get_by_username(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Incorrect username or password")

    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.password:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}
