from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Shared engine configuration
engine_params = {
    "pool_size": settings.DB_POOL_SIZE,
    "max_overflow": settings.DB_MAX_OVERFLOW,
    "pool_pre_ping": True,
    "connect_args": {"sslmode": settings.SSL_MODE},
}

# Create the SQLAlchemy engine using the connection string from settings
# The engine manages the connection pool to the database
# connect_args={"sslmode": "require"} enforces SSL for Supabase/Cloud Run
engine = create_engine(str(settings.DATABASE_URL), **engine_params)

# Create a configured "Session" class
# This factory will be used to create new Session objects for each request
# autocommit=False: We want to manually commit transactions
# autoflush=False: We want to manually flush changes to the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def set_custom_db_url(url: str) -> None:
    """
    Reconfigures the database engine and session maker with a custom URL.
    Useful for scripts requiring localhost connection instead of service names.
    """
    global engine
    engine.dispose()
    engine = create_engine(url, **engine_params)
    SessionLocal.configure(bind=engine)
