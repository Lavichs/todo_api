from pydantic import BaseModel


class SCredentials(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class SUserAdd(BaseModel):
    username: str
    password: bytes

    class Config:
        from_attributes = True


class SUser(SCredentials):
    id: int

