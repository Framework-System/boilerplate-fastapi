from datetime import datetime, timedelta
from typing import Annotated, Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from app.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    """
    Create access token.

    :param subject: subject of a token.
    :param expires_delta: expires_delta of a token.
    :return: token.
    """
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    return jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm,
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password.

    :param plain_password: plain_password.
    :param hashed_password: hashed_password.
    :return: bollean value.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Get password hash.

    :param password: password.
    :return: hash_password.
    """
    return pwd_context.hash(password)


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api_prefix}/v1/auth/access-token",
)


TokenDep = Annotated[str, Depends(reusable_oauth2)]


class TokenPayload(BaseModel):
    """
    Token Payload.

    Attributes:
        sub (str | None): Subject of the token.
    """

    sub: str | None = None
