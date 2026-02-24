import random
import string
import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Room, RoomPlayer
from app.models.room import GamePhase
from app.ws import broadcast

router = APIRouter(prefix="/rooms", tags=["rooms"])


def _generate_code() -> str:
    return "".join(random.choices(string.ascii_uppercase, k=4))


class CreateRoomRequest(BaseModel):
    host_id: uuid.UUID


class JoinRoomRequest(BaseModel):
    user_id: uuid.UUID


class AdvancePhaseRequest(BaseModel):
    host_id: uuid.UUID


@router.post("", status_code=201)
async def create_room(body: CreateRoomRequest, db: AsyncSession = Depends(get_db)):
    code = _generate_code()
    room = Room(code=code, host_id=body.host_id)
    db.add(room)
    # auto-add host as a player
    db.add(RoomPlayer(room=room, user_id=body.host_id))
    await db.commit()
    await db.refresh(room)
    return {"id": str(room.id), "code": room.code, "phase": room.phase}


async def _get_room_state(code: str, db: AsyncSession) -> dict:
    result = await db.execute(
        select(Room)
        .where(Room.code == code)
        .options(selectinload(Room.players).selectinload(RoomPlayer.user))
    )
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(404, "Room not found")
    return {
        "id": str(room.id),
        "code": room.code,
        "phase": room.phase,
        "host_id": str(room.host_id),
        "players": [
            {"id": str(p.user_id), "display_name": p.user.display_name}
            for p in room.players
        ],
    }


@router.get("/{code}")
async def get_room(code: str, db: AsyncSession = Depends(get_db)):
    return await _get_room_state(code, db)


@router.post("/{code}/join")
async def join_room(
    code: str, body: JoinRoomRequest, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Room).where(Room.code == code))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(404, "Room not found")
    if room.phase != GamePhase.waiting:
        raise HTTPException(400, "Game already started")
    db.add(RoomPlayer(room_id=room.id, user_id=body.user_id))
    await db.commit()
    state = await _get_room_state(code, db)
    await broadcast(code, {"type": "room_state", "data": state})
    return {"ok": True}


PHASE_ORDER = list(GamePhase)


@router.post("/{code}/advance")
async def advance_phase(
    code: str, body: AdvancePhaseRequest, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Room).where(Room.code == code))
    room = result.scalar_one_or_none()
    if not room:
        raise HTTPException(404, "Room not found")
    if room.host_id != body.host_id:
        raise HTTPException(403, "Only the host can advance the phase")
    idx = PHASE_ORDER.index(room.phase)
    if idx >= len(PHASE_ORDER) - 1:
        raise HTTPException(400, "Game already finished")
    room.phase = PHASE_ORDER[idx + 1]
    await db.commit()
    state = await _get_room_state(code, db)
    await broadcast(code, {"type": "room_state", "data": state})
    return {"phase": room.phase}
