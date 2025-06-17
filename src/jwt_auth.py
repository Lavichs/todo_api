from authx import AuthX, AuthXConfig, RequestToken

from config import settings

config = AuthXConfig(
    JWT_TOKEN_LOCATION=["cookies"],
    JWT_ACCESS_COOKIE_NAME="my_access_token",
    JWT_CSRF_METHODS=[]
)

# config = AuthXConfig()
config.JWT_SECRET_KEY = settings.JWT_SECRET_KEY
security = AuthX(config=config)
