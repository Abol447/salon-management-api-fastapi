from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class Token(Base):

    __tablename__ = "tokens"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )


    refresh_token = Column(
        String(500),
        nullable=False,
        unique=True,
        index=True
    )


    expires_at = Column(
        DateTime,
        nullable=False
    )


    is_revoked = Column(
        Boolean,
        default=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    user = relationship(
        "User",
        back_populates="tokens"
    )