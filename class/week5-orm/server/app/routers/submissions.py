import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Submission, Vote

router = APIRouter(prefix="/submissions", tags=["submissions"])


class CreateSubmissionRequest(BaseModel):
    prompt_id: uuid.UUID
    user_id: uuid.UUID
    body: str


class CastVoteRequest(BaseModel):
    user_id: uuid.UUID


@router.post("", status_code=201)
async def create_submission(
    body: CreateSubmissionRequest, db: AsyncSession = Depends(get_db)
):
    submission = Submission(
        prompt_id=body.prompt_id, user_id=body.user_id, body=body.body
    )
    db.add(submission)
    await db.commit()
    await db.refresh(submission)
    return {"id": str(submission.id)}


@router.get("/{submission_id}")
async def get_submission(
    submission_id: uuid.UUID, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Submission).where(Submission.id == submission_id)
    )
    sub = result.scalar_one_or_none()
    if not sub:
        raise HTTPException(404, "Submission not found")
    return {
        "id": str(sub.id),
        "prompt_id": str(sub.prompt_id),
        "user_id": str(sub.user_id),
        "body": sub.body,
    }


@router.post("/{submission_id}/vote", status_code=201)
async def vote_on_submission(
    submission_id: uuid.UUID,
    body: CastVoteRequest,
    db: AsyncSession = Depends(get_db),
):
    vote = Vote(submission_id=submission_id, user_id=body.user_id)
    db.add(vote)
    await db.commit()
    return {"ok": True}
