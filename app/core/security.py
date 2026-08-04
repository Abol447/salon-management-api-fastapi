from passlib.context import CryptContext
from app.core.config import settings
from jose import jwt, JWTError
from datetime import datetime, timedelta, UTC

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def create_token(data: dict ,  expire_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    expire = datetime.now(UTC)  + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    if(expire_delta):
        expire = expire +expire_delta

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        return payload

    except JWTError:
        return None