from fastapi import APIRouter, Depends

from ..schemas import user_schema
from ..dependencies import get_current_user

router = APIRouter()

# Endpoint to return information about the current user
@router.get("/", response_model=user_schema.User)
async def get_user(current_user: user_schema.User = Depends(get_current_user)):
    return current_user