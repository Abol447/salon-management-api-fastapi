from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    user_name = Column(String(100), unique=True, nullable=True)

    

    phone = Column(String(15), unique=True, nullable=False, index=True)

    email = Column(String(100), unique=True, nullable=True)

    password_hash = Column(String(255), nullable=False)

    is_active = Column(Boolean, default=True)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    role = relationship("Role", back_populates="users")

    tokens = relationship("Token", back_populates="user")

    customer = relationship("Customer", back_populates="user", uselist=False)

    owner = relationship("Owner", back_populates="user", uselist=False)
