import uuid
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=4,
    max_overflow=4,
)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)

async def get_async_session():
    async with async_session_maker() as session:
        yield session



class BaseModel(DeclarativeBase):
    pass


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    password: Mapped[bytes]
    tasks: Mapped[List["Task"]] = relationship()


class Task(BaseModel):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    status: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # created_at: Mapped[datetime] = mapped_column(default=datetime.now())

