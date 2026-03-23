from fastapi import Depends, HTTPException

from src.my_app.routers.auth_router import get_current_user


async def require_admin(current_user=Depends(get_current_user)): # This function can be used as a dependency in routes that require admin access (look admin_router.py)
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return current_user
