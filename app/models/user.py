import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base

class User(Base):
    """
    User model representing a registered user in the system.
    """
    __tablename__ = "users"

    # Primary Key: Unique identifier for the user (UUID)
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4
    )
    
    # Email: User's email address, must be unique
    email: Mapped[str] = mapped_column(String, unique=True, index=True)

    # Hashed Password: Securely stored password hash
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    
    # Created At: Timestamp when the user record was created
    # Server default ensures DB handles time
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    
    # Updated At: Timestamp of last update
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), nullable=True
    )