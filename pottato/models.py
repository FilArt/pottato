from uuid import uuid4

from sqlalchemy import Column, String, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from pottato.services.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)

    @classmethod
    async def create(cls, db: AsyncSession, **kwargs):
        if not kwargs.get("id"):
            kwargs["id"] = uuid4().hex

        transaction = cls(**kwargs)
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
        return transaction

    @classmethod
    async def get(cls, db: AsyncSession, id_: str):
        try:
            transaction = await db.get(cls, id_)
        except NoResultFound:
            return None
        return transaction

    @classmethod
    async def get_all(cls, db: AsyncSession):
        return (await db.execute(select(cls))).scalars().all()
