from datetime import datetime, timezone

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class User(Base):
    """
    User model representing a registered user in the system.
    """
    __tablename__ = "users"

    # Primary Key: Unique identifier for the user
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Email: User's email address, must be unique
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    
    # Created At: Timestamp when the user record was created
    # Defaults to the current UTC time
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )