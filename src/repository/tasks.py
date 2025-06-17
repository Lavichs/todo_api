from src.database.database import Task, async_session_maker, User
from sqlalchemy import insert, select, delete, update

from src.schemas.tasks import STask


class TaskRepository:
    model = Task

    async def create_task(self, data: dict) -> STask | None:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def find_all(self, offset: int, limit: int):
        async with async_session_maker() as session:
            stmt = select(self.model).offset(offset).limit(limit)
            res = await session.execute(stmt)
            res = [STask.model_validate(row[0]) for row in res.all()]
            return res

    async def get(self, id: int) -> STask | None:
        async with async_session_maker() as session:
            stmt = select(self.model).where(TaskRepository.model.id == id)
            result = await session.execute(stmt)
            post_model = result.scalar_one_or_none()
            if post_model is None:
                return None
            return STask.model_validate(post_model)

    async def delete(self, id: int) -> bool:
        async with async_session_maker() as session:
            stmt = delete(self.model).where(TaskRepository.model.id == id)
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount > 0

    async def update(self, id: int, data: dict) -> bool:
        async with async_session_maker() as session:
            stmt = (
                update(self.model)
                .where(TaskRepository.model.id == id)
                .values(**data)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount > 0
