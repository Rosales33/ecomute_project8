from datetime import datetime, timedelta, timezone
from typing import Any
from jose import jwt
from passlib.context import CryptContext

# En producción esto va en ENV VAR
SECRET_KEY = "LONG_RANDOM_SECRET_KEY_EXAMPLE_DO_NOT_USE_IN_PRODUCTION"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto") # pwd_context is an instance of CryptContext from the passlib library, which is used to handle password hashing and verification. In this case, we are using the "argon2" hashing algorithm.

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def create_access_token( # This function creates a JWT access token. It takes a dictionary of data to include in the token payload and an optional expiration time. If no expiration time is provided, it defaults to 60 minutes. The function encodes the data along with the expiration time using the SECRET_KEY and ALGORITHM defined earlier, and returns the encoded JWT token as a string.
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
