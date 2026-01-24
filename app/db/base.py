from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy models.

    It defines a common metadata object with naming conventions for constraints and indexes
    to ensure consistency and avoid auto-generated names that might be hard to manage in migrations.
    """

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",  # Index
            "uq": "uq_%(table_name)s_%(column_0_name)s",  # Unique constraint
            "ck": "ck_%(table_name)s_%(constraint_name)s",  # Check constraint
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  # Foreign key
            "pk": "pk_%(table_name)s",  # Primary key
        }
    )
