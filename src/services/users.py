from datetime import datetime, timedelta

import bcrypt

from config import settings
from src.jwt_auth import security
from src.repository.users import UserRepository
from src.schemas.users import SCredentials, SUser, SUserAdd


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def login(self, user: SCredentials) -> str | bool:
        candidate: SUser = await self.repository.get_by_username(user.username)
        if candidate is None:
            return False
        if bcrypt.checkpw(bytes(user.password, 'utf-8'), bytes(candidate.password, 'utf-8')):
            expire = datetime.now() + timedelta(minutes=settings.JWT_EXPIRATION_DELTA)
            token = security.create_access_token(uid=str(candidate.id), expires_delta=expire)
            return token
        else:
            return False

    async def sign_in(self, user: SCredentials) -> SUser:
        password = bytes(user.password, 'utf-8')
        user = SUserAdd(
            username=user.username,
            password=bcrypt.hashpw(password, bcrypt.gensalt())
        )
        return await self.repository.add(user.model_dump())

    # async def create_user(self, task: SUserAdd) -> SUser:
    #     return await self.repository.create_task(task.model_dump())
    #
    # async def get_all(self, offset: int = 0, limit: int = 100) -> List[SUser]:
    #     return await self.repository.find_all(offset=offset, limit=limit)
    #
    # async def get_one(self, id: int) -> SUser | None:
    #     return await self.repository.get(id)
    #
    # async def delete(self, id: int) -> bool:
    #     return await self.repository.delete(id)
    #
    # async def update(self, id: int, post: SUserAdd) -> bool:
    #     return await self.repository.update(id, post.model_dump())
