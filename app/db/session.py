from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create the SQLAlchemy engine using the connection string from settings
# The engine manages the connection pool to the database
engine = create_engine(str(settings.DATABASE_URL))

# Create a configured "Session" class
# This factory will be used to create new Session objects for each request
# autocommit=False: We want to manually commit transactions
# autoflush=False: We want to manually flush changes to the DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)