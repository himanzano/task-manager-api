import sys
import os

# Ensure the project root is in the python path
sys.path.append(os.getcwd())

from app.db.session import SessionLocal
from app.models.user import User
from app.models.task import Task, TaskStatus
from app.core.security import get_password_hash


def seed_data():
    # Uncomment and set the database URL if needed
    # set_custom_db_url("postgresql://postgres:postgres@localhost:5432/task_manager")
    db = SessionLocal()
    try:
        # Check if data already exists to avoid duplicates
        if db.query(User).first():
            print("Database already contains data. Skipping seed.")
            return

        print("Seeding database...")

        # Create Users
        user1 = User(
            email="alice@example.com", hashed_password=get_password_hash("password123")
        )
        user2 = User(
            email="bob@example.com", hashed_password=get_password_hash("securepass")
        )

        db.add(user1)
        db.add(user2)
        db.commit()
        db.refresh(user1)
        db.refresh(user2)

        # Create Tasks for User 1
        task1 = Task(
            title="Buy groceries",
            description="Milk, Bread, Eggs",
            status=TaskStatus.TODO,
            owner_id=user1.id,
        )
        task2 = Task(
            title="Walk the dog",
            description="Take the dog to the park",
            status=TaskStatus.DONE,
            owner_id=user1.id,
        )

        # Create Tasks for User 2
        task3 = Task(
            title="Complete project report",
            description="Finish the annual report analysis",
            status=TaskStatus.IN_PROGRESS,
            owner_id=user2.id,
        )

        db.add_all([task1, task2, task3])
        db.commit()

        print("Database seeded successfully!")
        print("Users created:")
        print(f" - {user1.email} (ID: {user1.id}) (password: password123)")
        print(f" - {user2.email} (ID: {user2.id}) (password: securepass)")

    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
