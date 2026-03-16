from fastapi import Depends, HTTPException

from src.my_app.routers.auth_router import get_current_user


async def require_admin(current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return current_user
