from fastapi import APIRouter, Depends, Header, HTTPException

from src.my_app.dependencies.auth import require_admin


def verify_admin_key(api_key: str = Header(...)): # This is a simple API key check
    if api_key != "eco-admin-secret":
        raise HTTPException(status_code=403, detail="Invalid admin API key")


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[
        Depends(verify_admin_key),
        Depends(require_admin)
    ],  # protects ALL endpoints here, router level dependency
)


@router.get("/stats")
async def get_admin_stats():
    return {"status": "ok", "message": "admin stats placeholder"}
