from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.my_app.db.database import get_db
from src.my_app.logger import logger
from src.my_app.repositories import users_repo
from src.my_app.schemas.auth import Token
from src.my_app.security import (
    ALGORITHM,
    SECRET_KEY,
    create_access_token,
    verify_password,
)

router = APIRouter(tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    logger.info("Login attempt for username=%s", form_data.username)
    # OAuth2PasswordRequestForm uses "username" field, we’ll treat it as username
    user = await users_repo.get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        logger.warning("Login failed for username=%s", form_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token({"sub": user.username}) # The create_access_token function is called to generate a JWT token for the authenticated user. The payload of the token includes a "sub" (subject) claim, which is set to the username of the authenticated user. This allows us to identify the user associated with the token when it is later used for authentication in protected routes.
    logger.info("Login successful for username=%s", user.username)
    return Token(access_token=token, token_type="bearer")


async def get_current_user( # This function can be used as a dependency in routes that require authentication
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    logger.info("Validating bearer token")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if not username:
            logger.warning("Token validation failed: missing subject")
            raise credentials_exception
    except JWTError:
        logger.warning("Token validation failed: invalid JWT")
        raise credentials_exception

    user = await users_repo.get_user_by_username(db, username)
    if not user:
        logger.warning("Token validation failed: user not found for username=%s", username)
        raise credentials_exception
    logger.info("Token validated for username=%s", username)
    return user
