# src/product.py
# Defines the Product data structure

class Product:
    def __init__(self, pid, name, category, price, rating, tags):
        self.id = pid
        self.name = name
        self.category = category
        self.price = price
        self.rating = rating
        self.tags = set(tags)  # Set for O(1) intersection in Jaccard

    def __repr__(self):
        return f"Product({self.id}, {self.name}, {self.category}, ₹{self.price}, ⭐{self.rating})"