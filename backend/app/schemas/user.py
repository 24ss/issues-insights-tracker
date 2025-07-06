from pydantic import BaseModel, EmailStr
from enum import Enum

class RoleEnum(str, Enum):
    admin = "ADMIN"
    maintainer = "MAINTAINER"
    reporter = "REPORTER"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum = RoleEnum.reporter

class UserRead(BaseModel):
    id: int
    email: EmailStr
    role: RoleEnum

    class Config:
        orm_mode = True
