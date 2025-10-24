import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv
import pandas as pd

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
    
    def description(self):
        """Return a list of column names."""
        return self.cursor.description if self.cursor else []
    
    def fetchone(self):
        """Fetch one row from the last executed SELECT query."""
        return self.cursor.fetchone() if self.cursor else None

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

def user_exists(email):
    try:
        check_query = sql.SQL("""
            SELECT 1 FROM users WHERE email = %s
        """)
        db.execute(check_query, (email,))
        exists = db.fetchone()
        print(f'{email} already exists') if exists else print(f'{email} does not exist')
        return exists is not None
    except Exception as e:
        print("❌ Failed to check user existence:", e)
        return False
  
    
def log_newuser(email, first_name=None, last_name=None):
    try: 
        insert_query = sql.SQL("""
            INSERT INTO users (email, first_name, last_name)
            VALUES (%s, %s, %s)
        """)
        db.execute(insert_query, (email, first_name, last_name))
    except Exception as e:
        print("❌ Failed to log user:", e)
    print("User logged successfully.")



def log_login(email, timestamp, device, first_name=None, last_name=None):
    try: 
        insert_query = sql.SQL("""
            INSERT INTO logins (email, timestamp, device, first_name, last_name)
            VALUES (%s, %s, %s, %s, %s)
        """)
        db.execute(insert_query, (email, timestamp, device, first_name, last_name))
    except Exception as e:
        print("❌ Failed to log login:", e)
    print("Login logged successfully.")
    
    
    
def log_message(message, timestamp, first=None, last=None):
    try: 
        insert_query = sql.SQL("""
            INSERT INTO messaging (message, timestamp, first_name, last_name)
            VALUES (%s, %s, %s, %s)
        """)
        db.execute(insert_query, (message, timestamp, first, last))
    except Exception as e:
        print("❌ Failed to log Message:", e)
    print("Message logged successfully.")

    
    
def query_message(first=None, last=None):
    try: 
        select_query = sql.SQL("""
            SELECT * 
            FROM messaging
            ORDER BY timestamp ASC
        """)
        db.execute(select_query)
        rows = db.fetchall()
        return rows
    except Exception as e:
        print("❌ Failed to query Messages:", e)
    print("Messages queried successfully.")
 
 
    
def check_permission(email, permission = None):
    try:
        check_query = sql.SQL("""
            SELECT 1 FROM user_access WHERE LOWER(email) = %s AND permission = %s
        """)
        db.execute(check_query, (email.lower(), permission,))
        user = db.fetchone()
        return user is not None
    except Exception as e:
        print("❌ Failed to check user existence:", e)
    return False



def store_users():
    try:
        user_query = sql.SQL("""
            SELECT * FROM users
        """)
        db.execute(user_query)
        users = db.fetchall()
        columns = [desc[0] for desc in db.description()]
        user_df = pd.DataFrame(users, columns = columns)
        return user_df
    except Exception as e:
        print("❌ Failed to pull users:", e)
        
  
def store_permissions():
    try:
        perm_query = sql.SQL("""
            SELECT * FROM permissions
        """)
        db.execute(perm_query)
        permissions = db.fetchall()
        columns = [desc[0] for desc in db.description()]
        permissions_df = pd.DataFrame(permissions, columns = columns)
        return permissions_df
    except Exception as e:
        print("❌ Failed to pull users:", e)
        
        
def permission_exists(email, permission):
    try:
        check_query = sql.SQL("""
            SELECT 1 FROM user_access WHERE email = %s AND permission = %s
        """)
        db.execute(check_query, (email, permission))
        permission_exists = db.fetchone()
        print(f'{permission_exists} already exists') if permission_exists else print(f'{permission_exists} does not exist')
        return permission_exists is not None
    except Exception as e:
        print("❌ Failed to check permission existence:", e)
        return False
    

        
def add_permissions(email, permission):
    try: 
        insert_query = sql.SQL("""
            INSERT INTO user_access (email, permission)
            VALUES (%s, %s)
        """)
        db.execute(insert_query, (email, permission))
    except Exception as e:
        print("❌ Failed to add permission:", e)
    print("Permission added successfully.")
    
    
    
def remove_permissions(email, permission):
    try: 
        delete_query = sql.SQL("""
            DELETE FROM user_access
            WHERE email = %s AND permission = %s
        """)
        db.execute(delete_query, (email, permission))
    except Exception as e:
        print("❌ Failed to delete permission:", e)
    print("Permission deleted successfully.")

    
def store_user_permissions():
    try:
        query = sql.SQL("""
            SELECT users.email, user_access.permission
            FROM users
            LEFT JOIN user_access
                ON users.email = user_access.email
        """)
        db.execute(query)
        permissions = db.fetchall()
        user_permissions = {}
        for row in permissions:
            email, permission = row
            if email not in user_permissions:
                user_permissions[email] = []
            user_permissions[email].append(permission)
        
        return user_permissions
    except Exception as e:
        print("❌ Failed to pull user permissons:", e)    
        

def query_logins():
    try: 
        select_query = sql.SQL("""
            SELECT * 
            FROM logins
            ORDER BY timestamp DESC
        """)
        db.execute(select_query)
        rows = db.fetchall()
        return rows
    except Exception as e:
        print("❌ Failed to query Messages:", e)
    print("Messages queried successfully.")
   
    
def insert_vendor(landlord, request_date, requester, vcode, w9, fed_class, ownership_proof, owner_declaration, disclosure, direct_deposit, canceled_check, creator, compliance_date, approver, status, approved_date, email, request_id):
    try: 
        insert_query = sql.SQL("""
            INSERT INTO vendor_requests (
            landlord, 
            request_date, 
            requester, 
            vcode,
            w9,
            fed_class,
            ownership_proof,
            owner_declaration,
            disclosure,
            direct_deposit,
            canceled_check,
            creator,
            compliance_date,
            approver,
            status,
            approved_date,
            email,
            request_id
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """)
        db.execute(insert_query, (
            landlord, 
            request_date, 
            requester, 
            vcode, 
            w9, 
            fed_class, 
            ownership_proof, 
            owner_declaration, 
            disclosure, 
            direct_deposit, 
            canceled_check, 
            creator, 
            compliance_date, 
            approver, 
            status, 
            approved_date, 
            email,
            request_id
            )
            )
    except Exception as e:
        print("❌ Failed to log Vendor Request:", e)
    print("Vendor Request logged successfully.")

def update_vendor_cell(request_id, column_name, new_value):
    try: 
        update_query = sql.SQL("""
            UPDATE vendor_requests
            SET {column} = %s
            WHERE request_id = %s
        """).format(column=sql.Identifier(column_name))
        db.execute(update_query, (new_value, request_id))
    except Exception as e:
        print("❌ Failed to update Vendor Request:", e)
    print("Vendor Request updated successfully.")
    
def query_vendor_requests():
    try: 
        select_query = sql.SQL("""
            SELECT * 
            FROM vendor_requests
            ORDER BY request_date ASC
        """)
        db.execute(select_query)
        rows = db.fetchall()
        return rows
    except Exception as e:
        print("❌ Failed to query Messages:", e)
    print("Messages queried successfully.")
    
    
def check_pending_vendor():
    try: 
        select_query = sql.SQL("""
            SELECT status 
            FROM vendor_requests
        """)
        db.execute(select_query)
        rows = db.fetchall()
        return rows
    except Exception as e:
        print("❌ Failed to query Messages:", e)
    print("Messages queried successfully.")
   