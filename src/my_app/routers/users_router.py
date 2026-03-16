from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.my_app.db.database import get_db
from src.my_app.repositories import users_repo
from src.my_app.schemas.users import UserSignup, UserUpdate, UserResponse
from src.my_app.security import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    return await users_repo.list_users(db)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await users_repo.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/signup", response_model=UserResponse, status_code=201)
async def signup(payload: UserSignup, db: AsyncSession = Depends(get_db)):
    # prevent duplicates
    existing = await users_repo.get_user_by_username(db, payload.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed = get_password_hash(payload.password)
    user = await users_repo.create_user(
        db,
        username=payload.username,
        email=str(payload.email),
        hashed_password=hashed,
        role="rider",
    )
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, payload: UserUpdate, db: AsyncSession = Depends(get_db)
):
    updated = await users_repo.update_user(
        db, user_id, payload.model_dump(exclude_unset=True)
    )
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    ok = await users_repo.delete_user(db, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return None
