# src/user.py
# Defines the User data structure

class User:
    def __init__(self, uid, name, age, interests):
        self.id = uid
        self.name = name
        self.age = age
        self.interests = interests       # List of preferred categories
        self.purchased = []              # Product IDs bought
        self.cart = []                   # Product IDs in cart
        self.searched = []               # Product IDs searched
        self.ratings = {}                # product_id → rating score

    def load_interactions(self, interactions):
        """Load interaction data from interactions dictionary"""
        data = interactions.get(self.id, {})
        self.purchased = data.get("purchased", [])
        self.cart = data.get("cart", [])
        self.searched = data.get("searched", [])
        self.ratings = data.get("ratings", {})

    def __repr__(self):
        return f"User({self.id}, {self.name})"