from datetime import datetime, timezone

from sqlalchemy import(
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from SERVER.persistance.database import Base

class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True
    )

    user_id: Mapped[str] = mapped_column(
        String(100),
        index=True,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="active"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    messages: Mapped[list["Message"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="Message.created_at",
    )

class Message(Base):
        __tablename__ = "messages"

        id: Mapped[int] = mapped_column(
            Integer,
            primary_key=True,
            autoincrement=True
        )

        sesssion_id: Mapped[str] = mapped_column(
            ForeignKey("sessions.id"),
            nullable=False,
            index=True
        )

        role: Mapped[str] = mapped_column(
            String(20),
            nullable=False,
        )

        content: Mapped[str] = mapped_column(
            Text,
            nullable=False,
        )

        created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc),
        )

        session: Mapped["Session"] = relationship(
            back_populates="messages",
        )

