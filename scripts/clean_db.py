import sys
import os

# Ensure the project root is in the python path
sys.path.append(os.getcwd())

from sqlalchemy import text
from app.db.session import SessionLocal


def clean_database():
    """
    Deletes all data from the database tables.
    """
    # Uncomment and set the database URL if needed
    # set_custom_db_url("postgresql://postgres:postgres@localhost:5432/task_manager")
    db = SessionLocal()
    try:
        print("Cleaning database...")

        # Use TRUNCATE with CASCADE to clear tables and handle relationships
        # This is more efficient than DELETE. RESTART IDENTITY is not needed for UUIDs.
        db.execute(text("TRUNCATE TABLE tasks, users CASCADE;"))
        db.commit()

        print("Database cleaned successfully!")

    except Exception as e:
        print(f"Error cleaning database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    confirmation = input("Are you sure you want to delete ALL data? (y/N): ")
    if confirmation.lower() == "y":
        clean_database()
    else:
        print("Operation cancelled.")
