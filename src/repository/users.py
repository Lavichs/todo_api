from src.database.database import async_session_maker, User
from sqlalchemy import insert, select

from src.schemas.users import SUser


class UserRepository:
    model = User
    
    async def add(self, data: dict) -> SUser:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def get_by_id(self, id: int) -> SUser | None:
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.id == id)
            result = await session.execute(stmt)
            post_model = result.scalar_one_or_none()
            if post_model is None:
                return None
            return SUser.model_validate(post_model)

    async def get_by_username(self, username: str) -> SUser | None:
        async with async_session_maker() as session:
            stmt = select(self.model).where(self.model.username == username).limit(1)
            result = await session.execute(stmt)
            post_model = result.scalar_one_or_none()
            if post_model is None:
                return None
            return SUser.model_validate(post_model)
