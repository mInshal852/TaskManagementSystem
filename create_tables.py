from app.database.base import Base
from app.database.connection import engine

# Import the models so they register with Base.metadata
import app.models.user  # noqa: F401
import app.models.task  # noqa: F401


def create_tables():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully (or already exist).")


if __name__ == "__main__":
    create_tables()


# Linter
#   ↓
# Checks your code

# F401
#   ↓
# "Imported but not used"

# # noqa: F401
#   ↓
# "Yes, I know. Ignore this warning."
