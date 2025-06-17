from pydantic import BaseModel

class STaskAdd(BaseModel):
    title: str
    description: str
    status: str

    class Config:
        from_attributes = True


class STaskAddInDB(STaskAdd):
    user_id: int


class STask(STaskAdd):
    id: int
