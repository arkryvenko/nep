from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, example="jonsnow")
    first_name: str = Field(..., min_length=3, max_length=50, example="Jon")
    last_name: str = Field(..., min_length=3, max_length=50, example="Snow")
    email: EmailStr = Field(..., example="jon.snow@winterfell.com")
    country: str = Field(..., example="North")


class UserInDB(UserBase):
    password: str


class UserOut(UserBase):
    id: int
