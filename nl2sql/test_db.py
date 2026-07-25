from database import Database

db = Database()

if db.test_connection():
    print("PostgreSQL connection successful!")