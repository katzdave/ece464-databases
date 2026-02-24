import enum
import uuid

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class GamePhase(str, enum.Enum):
    waiting = "waiting"
    prompting = "prompting"
    submitting = "submitting"
    voting = "voting"
    results = "results"
    finished = "finished"


class Room(Base):
    __tablename__ = "rooms"

    code: Mapped[str] = mapped_column(String(4), unique=True, nullable=False, index=True)
    phase: Mapped[GamePhase] = mapped_column(
        Enum(GamePhase), default=GamePhase.waiting, nullable=False
    )
    host_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )

    host: Mapped["User"] = relationship()
    players: Mapped[list["RoomPlayer"]] = relationship(back_populates="room")
    prompts: Mapped[list["Prompt"]] = relationship(back_populates="room")
