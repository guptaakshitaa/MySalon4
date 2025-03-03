class Salon:
    """Represents a Salon entity with relevant attributes."""

    def __init__(self, salon_id, name, address, location, category, rating):
        self.id = salon_id
        self.name = name
        self.address = address
        self.location = location
        self.category = category
        self.rating = rating

    def __str__(self):
        return f"{self.name} ({self.rating}⭐) - {self.address}, {self.location} - {self.category}"
