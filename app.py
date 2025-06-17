from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.database.database import (delete_tables, create_tables)
from src.routes.tasks import router as tasks_router
from src.routes.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("База очищена")
    await create_tables()
    print("База готова")
    yield
    print("Выключение")
app = FastAPI(
    lifespan=lifespan,
    openapi_url="/core/openapi.json",
    docs_url="/core/docs",
)

app.include_router(users_router)
app.include_router(tasks_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
