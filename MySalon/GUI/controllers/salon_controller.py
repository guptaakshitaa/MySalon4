from config.database import get_database_connection
from models.salon import Salon

class SalonController:
    def __init__(self):
        """Initialize database connection."""
        self.conn = get_database_connection()

    def get_top_salons(self):
        """Retrieve top 5 highest-rated salons."""
        if not self.conn:
            return []
        
        try:
            c = self.conn.cursor()
            query = "SELECT SalonID, Name, Address, Location, ContactNumber, Rating FROM Salons ORDER BY rating DESC"
            c.execute(query)
            results = c.fetchall()
            c.close()

            return [Salon(*salon) for salon in results]  # Convert to Salon objects
        except Exception as e:
            print(f"❌ Error fetching top salons: {e}")
            return []

    def search_salons(self, search_query, filter_type):
        """Search salons based on Name, Service, or Location."""
        if not self.conn:
            return []

        try:
            column_mapping = {
                "Name": "Name",
                "Service": "Service",
                "Location": "Location",
            }
            column_name = column_mapping.get(filter_type.lower(), "name")

            c = self.conn.cursor()
            query = f"SELECT SalonID, Name, Address, Location, ContactNumber, Rating FROM Salons WHERE {column_name} LIKE %s"
            c.execute(query, (f"%{search_query}%",))
            results = c.fetchall()
            c.close()

            return [Salon(*salon) for salon in results]  # Convert to objects
        except Exception as e:
            print(f"❌ Error searching salons: {e}")
            return []
