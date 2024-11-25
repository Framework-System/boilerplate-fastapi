from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.routes.v1.auth.dtos import Token
from app.middlewares.auth.deps import authenticate
from app.middlewares.auth.security import create_access_token
from app.settings import settings

# Define the API router for user models.
router = APIRouter()


@router.post("/access-token")
async def access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests.

    :param form_data: OAuth2 compatible login form data.
    :return: access token for future requests.
    :raises HTTPException: If the user doesn't have enough privileges.
    """
    user = await authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    return Token(
        access_token=create_access_token(user.id, expires_delta=access_token_expires),
    )
