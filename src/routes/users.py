from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Response

from src.jwt_auth import config, security
from src.schemas.users import SCredentials
from src.services.users import UserService
from src.utils.depends import get_user_service

router = APIRouter(prefix="/users", tags=["users"])


# @router.post("")
# async def create(
#         user: Annotated[SUserAdd, Depends()],
#         user_service: UserService = Depends(get_user_service),
# ) -> SUser:
#     user = await user_service.create_user(user)
#     return user

@router.get("/login")
async def login(
        response: Response,
        credentials: Annotated[SCredentials, Depends()],
        user_service: UserService = Depends(get_user_service),
):
    token = await user_service.login(credentials)
    if token:
        security.set_access_cookies(response=response, token=token)
        # response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {config.JWT_ACCESS_COOKIE_NAME: token}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

# if username == "test" and password == "test":
#         token = security.create_access_token(uid=username)
#         return {"access_token": token}
#     raise HTTPException(401, detail={"message": "Bad credentials"})

@router.get("/sign_in", status_code=201)
async def login(
        credentials: Annotated[SCredentials, Depends()],
        user_service: UserService = Depends(get_user_service)
) -> bool:
    await user_service.sign_in(credentials)
    return True
