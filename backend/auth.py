import base64
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

import exceptions
import models
import settings

SECRET = settings.SECRET_KEY
DIGEST = "sha256"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


async def get_user(email: str):
    return await models.User.objects.get_or_none(email=email)


def create_password_hash(password: str):
    secret = hashlib.sha256(SECRET.encode()).digest()
    secret = base64.urlsafe_b64encode(secret)
    return hashlib.sha512(secret + password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str):
    new_hash = create_password_hash(plain_password)
    return hmac.compare_digest(new_hash, hashed_password)


async def authenticate_user(email: str, password: str):
    user = await get_user(email=email)
    if not user:
        return False

    if not verify_password(password, user.password):
        return False

    return user


def create_access_token(user: dict, data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(tz=settings.TIMEZONE) + expires_delta
    else:
        expire = datetime.now(tz=settings.TIMEZONE) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        SECRET,
        algorithm=ALGORITHM,
        headers={
            "user": user,
        }
    )


def check_user_auth(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise exceptions.INCORRECT_LOGIN_DATA_EXCEPTION

    except jwt.exceptions.PyJWTError:
        raise exceptions.INCORRECT_LOGIN_DATA_EXCEPTION  # noqa: B904

    return email


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    email = check_user_auth(token)

    user = await get_user(email=email)
    if user is None:
        raise exceptions.INCORRECT_LOGIN_DATA_EXCEPTION

    return user


def create_token(user: models.User):
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {"sub": user.email}
    access_token = create_access_token(
        user=user.model_dump(exclude={"date_joined"}),
        data=data,
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "Bearer"}


UserType = Annotated[models.User, Depends(get_current_user)]
