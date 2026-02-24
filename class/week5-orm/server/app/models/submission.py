import uuid

from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Submission(Base):
    __tablename__ = "submissions"

    prompt_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("prompts.id"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    body: Mapped[str] = mapped_column(Text, nullable=False)

    prompt: Mapped["Prompt"] = relationship(back_populates="submissions")
    user: Mapped["User"] = relationship(back_populates="submissions")
    votes: Mapped[list["Vote"]] = relationship(back_populates="submission")
