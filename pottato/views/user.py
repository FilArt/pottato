from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession

from pottato.services.database import get_db

from pottato.models import User as UserModel

router = APIRouter(prefix="/user", tags=["user"])


class UserSchemaBase(BaseModel):
    email: str | None = None
    full_name: str | None = None


class UserSchemaCreate(UserSchemaBase):
    pass


class UserSchema(UserSchemaBase):
    id: str
    model_config = ConfigDict(from_attributes=True)


@router.get("/get-user", response_model=UserSchema)
async def get_user(id: str, db: AsyncSession = Depends(get_db)):  # pylint: disable=redefined-builtin
    user = await UserModel.get(db, id)
    return user


@router.get("/get-users", response_model=list[UserSchema])
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await UserModel.get_all(db)
    return users


@router.post("/create-user", response_model=UserSchema)
async def create_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_db)):
    user = await UserModel.create(db, **user.model_dump())
    return user
