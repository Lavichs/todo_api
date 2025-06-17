from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException

from src.jwt_auth import security
from src.schemas.tasks import STask, STaskAdd
from src.services.tasks import TaskService
from src.utils.depends import get_task_service
from authx import RequestToken, TokenPayload

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("")
async def get_all(
        offset: int = 0,
        limit: int = 10,
        task_service: TaskService = Depends(get_task_service),
) -> List[STask]:
    tasks = await task_service.get_all(offset, limit)
    return tasks


@router.get("/{id}")
async def get_task(
        id: int,
        task_service: TaskService = Depends(get_task_service),
) -> STask | None:
    task = await task_service.get_one(id)
    return task


@router.post("", dependencies=[Depends(security.access_token_required)])
async def create(
        task: Annotated[STaskAdd, Depends()],
        task_service: TaskService = Depends(get_task_service),
        payload: TokenPayload = Depends(security.access_token_required)
) -> STask:
    try:
        task = await task_service.create_task(task=task, user_id=int(payload.sub))
        return task
    except Exception as e:
        raise HTTPException(401, detail={"message": str(e)}) from e

@router.delete("/{id}", dependencies=[Depends(security.access_token_required)])
async def delete(
        id: int,
        task_service: TaskService = Depends(get_task_service),
) -> bool:
    res = await task_service.delete(id)
    return res

@router.put("/{id}", dependencies=[Depends(security.access_token_required)])
async def update(
        id: int,
        task: Annotated[STaskAdd, Depends()],
        task_service: TaskService = Depends(get_task_service),
) -> bool:
    res = await task_service.update(id, task)
    return res
