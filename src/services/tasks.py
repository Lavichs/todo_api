from typing import List

from src.repository.tasks import TaskRepository
from src.schemas.tasks import STaskAdd, STask, STaskAddInDB


class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    async def create_task(self, task: STaskAdd, user_id: int) -> STask:
        task_to_db = STaskAddInDB(**task.model_dump(), user_id=user_id)
        return await self.repository.create_task(task_to_db.model_dump())

    async def get_all(self, offset: int = 0, limit: int = 100) -> List[STask]:
        return await self.repository.find_all(offset=offset, limit=limit)

    async def get_one(self, id: int) -> STask | None:
        return await self.repository.get(id)

    async def delete(self, id: int) -> bool:
        return await self.repository.delete(id)

    async def update(self, id: int, post: STaskAdd) -> bool:
        return await self.repository.update(id, post.model_dump())
