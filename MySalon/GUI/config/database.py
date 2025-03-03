import mysql.connector

def get_database_connection():
    """Establish and return a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='new12345',  # Change if needed
            database='salonMumbai'
        )
        print("✅ Connected to MySQL database salonMumbai")
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
        return None
