from http import HTTPStatus
from passlib.context import CryptContext

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from api.models import UserInDB
from api.crud import get_by_username


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_db = await get_by_username(form_data.username)
    if not user_db:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Incorrect username or password")

    user = UserInDB(**user_db)
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}
