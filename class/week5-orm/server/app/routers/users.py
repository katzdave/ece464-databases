import uuid
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import User

router = APIRouter(prefix="/users", tags=["users"])


class CreateUserRequest(BaseModel):
    display_name: str
    avatar_url: Optional[str] = ""


@router.post("", status_code=201)
async def create_user(body: CreateUserRequest, db: AsyncSession = Depends(get_db)):
    user = User(
        supabase_id=f"guest-{uuid.uuid4()}",
        display_name=body.display_name,
        avatar_url=body.avatar_url or "",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"id": str(user.id), "display_name": user.display_name}
