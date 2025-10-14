import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseController:
    def __init__(self, dbname, user, password, host="localhost", port=5432):
        self.connection = None
        self.cursor = None
        self.config = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port
        }

    def connect(self):
        """Establish a connection to the PostgreSQL database."""
        try:
            self.connection = psycopg2.connect(**self.config)
            self.cursor = self.connection.cursor()
            print("✅ Connected to database.")
        except Exception as e:
            print("❌ Database connection failed:", e)

    def execute(self, query, params=None):
        """Execute a query (INSERT, UPDATE, DELETE, SELECT, etc.)."""
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            print("✅ Query executed successfully.")
        except Exception as e:
            print("❌ Query failed:", e)
            self.connection.rollback()

    def fetchall(self):
        """Fetch all rows from the last executed SELECT query."""
        return self.cursor.fetchall() if self.cursor else []

    def close(self):
        """Close the cursor and database connection."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("🔒 Database connection closed.")



db = DatabaseController(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

# Connect to database
db.connect()

def log_login(email, timestamp, device):
    try: 
        insert_query = sql.SQL("""
            INSERT INTO logins (email, timestamp, device)
            VALUES (%s, %s, %s)
        """)
        db.execute(insert_query, (email, timestamp, device))
    except Exception as e:
        print("❌ Failed to log login:", e, f'Database Controller State: {db.config}')
    print("Login logged successfully.")