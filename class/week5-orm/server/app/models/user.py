from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    supabase_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(50), nullable=False)
    avatar_url: Mapped[str] = mapped_column(String, nullable=False)

    room_players: Mapped[list["RoomPlayer"]] = relationship(back_populates="user")
    submissions: Mapped[list["Submission"]] = relationship(back_populates="user")
    votes: Mapped[list["Vote"]] = relationship(back_populates="user")
