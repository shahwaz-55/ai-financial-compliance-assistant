
from backend.database.database import create_tables, test_database_connection

if __name__ == "__main__":
    print("Database connection result:", test_database_connection())
    create_tables()
    print("Database tables created successfully!")
