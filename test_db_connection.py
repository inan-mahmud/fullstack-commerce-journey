"""
Simple script to test database connection.
Run this to verify PostgreSQL is accessible and configured correctly.
"""

from app.database import engine
from sqlalchemy import text


def test_connection():
    """Test database connection and print PostgreSQL version."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print("✅ Database connection successful!")
            print(f"📦 PostgreSQL version: {version}")
            return True
    except Exception as e:
        print("❌ Database connection failed!")
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    test_connection()
