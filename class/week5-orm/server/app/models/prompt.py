import uuid

from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Prompt(Base):
    __tablename__ = "prompts"

    room_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("rooms.id"), nullable=False
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)

    room: Mapped["Room"] = relationship(back_populates="prompts")
    submissions: Mapped[list["Submission"]] = relationship(back_populates="prompt")
